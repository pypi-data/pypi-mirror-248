import os
# work with proc_per_node 2
# os.environ["CUDA_VISIBLE_DEVICES"] = "0,2"
import torch
import contextlib
from torch.nn.parallel import DistributedDataParallel as DDP
import torch.distributed as dist
import pkg_resources as pkg
from contextlib import contextmanager
from torch.cuda import amp
from datetime import datetime
from tqdm import tqdm
import math
from copy import deepcopy
import torch.nn as nn
from aicmder.utils import colorstr
from pathlib import Path
torch.backends.cudnn.benchmark = True

LOCAL_RANK = int(os.getenv('LOCAL_RANK', -1))  # https://pytorch.org/docs/stable/elastic/run.html
RANK = int(os.getenv('RANK', -1))
WORLD_SIZE = int(os.getenv('WORLD_SIZE', 1))


def smart_optimizer(model, name='Adam', lr=0.001, momentum=0.9, decay=1e-5):
    # YOLOv5 3-param group optimizer: 0) weights with decay, 1) weights no decay, 2) biases no decay
    g = [], [], []  # optimizer parameter groups
    bn = tuple(v for k, v in nn.__dict__.items() if 'Norm' in k)  # normalization layers, i.e. BatchNorm2d()
    for idx, v in enumerate(model.modules()):
        # weight and bias, here add bias
        if hasattr(v, 'bias') and isinstance(v.bias, nn.Parameter):  # bias (no decay)
            g[2].append(v.bias)

        # add weight
        if isinstance(v, bn):  # weight (no decay)
            g[1].append(v.weight)
        elif hasattr(v, 'weight') and isinstance(v.weight, nn.Parameter):  # weight (with decay)
            g[0].append(v.weight)

    if name == 'Adam':
        optimizer = torch.optim.Adam(g[2], lr=lr, betas=(momentum, 0.999))  # adjust beta1 to momentum
    elif name == 'AdamW':
        optimizer = torch.optim.AdamW(g[2], lr=lr, betas=(momentum, 0.999), weight_decay=0.0)
    elif name == 'RMSProp':
        optimizer = torch.optim.RMSprop(g[2], lr=lr, momentum=momentum)
    elif name == 'SGD':
        optimizer = torch.optim.SGD(g[2], lr=lr, momentum=momentum, nesterov=True)
    else:
        raise NotImplementedError(f'Optimizer {name} not implemented.')

    optimizer.add_param_group({'params': g[0], 'weight_decay': decay})  # add g0 with weight_decay
    optimizer.add_param_group({'params': g[1], 'weight_decay': 0.0})  # add g1 (BatchNorm2d weights)
    print(f"{colorstr('optimizer:')} {type(optimizer).__name__}(lr={lr}) with parameter groups "
                f"{len(g[1])} weight(decay=0.0), {len(g[0])} weight(decay={decay}), {len(g[2])} bias")
    return optimizer

class EarlyStopping:
    # YOLOv5 simple early stopper
    def __init__(self, evaluate_func, patience=30):
        self.best_fitness = None  # i.e. mAP
        self.best_epoch = 0
        self.patience = patience or float('inf')  # epochs to wait after fitness stops improving to stop
        self.possible_stop = False  # possible stop may occur next epoch
        self.evaluate_func = evaluate_func

    def __call__(self, epoch, fitness):
        if self.best_fitness is None:
            self.best_fitness = fitness
            
        if self.evaluate_func(fitness, self.best_fitness):  # >= 0 to allow for early zero-fitness stage of training
            self.best_epoch = epoch
            self.best_fitness = fitness
        delta = epoch - self.best_epoch  # epochs without improvement
        self.possible_stop = delta >= (self.patience - 1)  # possible stop may occur next epoch
        stop = delta >= self.patience  # stop training if patience exceeded
        if stop:
            print(f'Stopping training early as no improvement observed in last {self.patience} epochs. '
                        f'Best results observed at epoch {self.best_epoch}, best model saved as best.pt.\n'
                        f'To update EarlyStopping(patience={self.patience}) pass a new patience value, '
                        f'i.e. `python train.py --patience 300` or use `--patience 0` to disable EarlyStopping.')
        return stop



def copy_attr(a, b, include=(), exclude=()):
    # Copy attributes from b to a, options to only include [...] and to exclude [...]
    for k, v in b.__dict__.items():
        if (len(include) and k not in include) or k.startswith('_') or k in exclude:
            continue
        else:
            setattr(a, k, v)


def is_parallel(model):
    # Returns True if model is of type DP or DDP
    return type(model) in (nn.parallel.DataParallel, nn.parallel.DistributedDataParallel)


def de_parallel(model):
    # De-parallelize a model: returns single-GPU model if model is of type DP or DDP
    return model.module if is_parallel(model) else model


@contextmanager
def torch_distributed_zero_first(local_rank: int):
    """
    Decorator to make all processes in distributed training wait for each local_master to do something.
    use LOCAL_RANK here for creating dataset and distributed.DistributedSampler to sample dataset
    """
    if local_rank not in [-1, 0]:
        dist.barrier(device_ids=[local_rank])
    yield
    if local_rank == 0:
        dist.barrier(device_ids=[0])


def check_version(current='0.0.0', minimum='0.0.0', name='version ', pinned=False, hard=False, verbose=False):
    # Check version vs. required version
    current, minimum = (pkg.parse_version(x) for x in (current, minimum))
    result = (current == minimum) if pinned else (current >= minimum)  # bool
    # s = f'{name}{minimum} required by YOLOv5, but {name}{current} is currently installed'  # string
    if hard:
        assert result  # assert min requirements met
    # if verbose and not result:
    #     LOGGER.warning(s)
    return result


def smart_inference_mode(torch_1_9=check_version(torch.__version__, '1.9.0')):
    # Applies torch.inference_mode() decorator if torch>=1.9.0 else torch.no_grad() decorator
    def decorate(fn):
        return (torch.inference_mode if torch_1_9 else torch.no_grad)()(fn)

    return decorate


class DPModel(contextlib.ContextDecorator):
    def __init__(self, model):
        # self.devices = devices
        # os.environ["CUDA_VISIBLE_DEVICES"] = self.devices
        self.gpu_count = torch.cuda.device_count()
        self.model = model

    def __enter__(self):
        if self.gpu_count > 1:
            return torch.nn.DataParallel(self.model)
        else:
            return self.model

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def smart_DDP(model):
    # Model DDP creation with checks
    assert not check_version(torch.__version__, '1.12.0', pinned=True), \
        'torch==1.12.0 torchvision==0.13.0 DDP training is not supported due to a known issue. ' \
        'Please upgrade or downgrade torch to use DDP. See https://github.com/ultralytics/yolov5/issues/8395'
    if check_version(torch.__version__, '1.11.0'):
        return DDP(model, device_ids=[LOCAL_RANK], output_device=LOCAL_RANK, static_graph=True)
    else:
        return DDP(model, device_ids=[LOCAL_RANK], output_device=LOCAL_RANK)


class DDPModel(contextlib.ContextDecorator):
    def __init__(self, model, devices=None, auto_clean=True):
        self.devices = devices
        # os.environ["CUDA_VISIBLE_DEVICES"] = self.devices
        # self.gpu_count = torch.cuda.device_count()
        self.model = model
        self.auto_clean = auto_clean

    def __enter__(self):
        if LOCAL_RANK != -1:
            assert torch.cuda.device_count() > LOCAL_RANK, 'insufficient CUDA devices for DDP command'
            torch.cuda.set_device(LOCAL_RANK)
            device = torch.device('cuda', LOCAL_RANK)
            dist.init_process_group(backend="nccl" if dist.is_nccl_available() else "gloo")
            self.model.to(device)
            cuda = device.type != 'cpu'
            if cuda and RANK != -1:
                return smart_DDP(self.model), device
        self.model.to(self.devices)
        return self.model, self.devices

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def cleanup(self):
        if WORLD_SIZE > 1 and RANK == 0 and self.auto_clean:
            dist.destroy_process_group()


def check_amp(model):
    # Check PyTorch Automatic Mixed Precision (AMP) functionality. Return True on correct operation

    def amp_allclose(model):
        model = model.eval()

        # All close FP32 vs AMP results
        first_parameter = next(model.parameters())
        input_shape = first_parameter.size()
        model_input = torch.zeros(input_shape, device=next(model.parameters()).device).contiguous()  # input
        a = model(model_input)  # FP32 inference

        with amp.autocast(True):
            b = model(model_input)  # AMP inference
        return a.shape == b.shape and torch.allclose(a, b, atol=0.1)  # close to 10% absolute tolerance

    # prefix = colorstr('AMP: ')
    device = next(model.parameters()).device  # get model device
    if device.type == 'cpu':
        return False  # AMP disabled on CPU
    # f = ROOT / 'data' / 'images' / 'bus.jpg'  # image to check
    # im = f if f.exists() else 'https://ultralytics.com/images/bus.jpg' if check_online() else np.ones((640, 640, 3))
    try:
        assert amp_allclose(model)
        # LOGGER.info(emojis(f'{prefix}checks passed ✅'))
        return True
    except Exception as e:
        print("check_amp assert:", e)
        # help_url = 'https://github.com/ultralytics/yolov5/issues/7908'
        # LOGGER.warning(emojis(f'{prefix}checks failed ❌, disabling Automatic Mixed Precision. See {help_url}'))
        return False


class ModelEMA:
    """ Updated Exponential Moving Average (EMA) from https://github.com/rwightman/pytorch-image-models
    Keeps a moving average of everything in the model state_dict (parameters and buffers)
    For EMA details see https://www.tensorflow.org/api_docs/python/tf/train/ExponentialMovingAverage
    """

    def __init__(self, model, decay=0.9999, tau=2000, updates=0):
        # Create EMA
        self.ema = deepcopy(de_parallel(model)).eval()  # FP32 EMA
        self.updates = updates  # number of EMA updates
        self.decay = lambda x: decay * (1 - math.exp(-x / tau))  # decay exponential ramp (to help early epochs)
        for p in self.ema.parameters():
            p.requires_grad_(False)

    def update(self, model):
        # Update EMA parameters
        self.updates += 1
        d = self.decay(self.updates)

        msd = de_parallel(model).state_dict()  # model state_dict
        for k, v in self.ema.state_dict().items():
            if v.dtype.is_floating_point:  # true for FP16 and FP32
                v *= d
                v += (1 - d) * msd[k].detach()
        # assert v.dtype == msd[k].dtype == torch.float32, f'{k}: EMA {v.dtype} and model {msd[k].dtype} must be FP32'

    def update_attr(self, model, include=(), exclude=('process_group', 'reducer')):
        # Update EMA attributes
        copy_attr(self.ema, model, include, exclude)


def smart_resume(ckpt, optimizer, ema=None, epochs=300, resume=True):
    # Resume training from a partially trained checkpoint
    best_fitness = None
    start_epoch = ckpt['epoch'] + 1
    if ckpt['optimizer'] is not None:
        optimizer.load_state_dict(ckpt['optimizer'])  # optimizer
        best_fitness = ckpt['best_fitness']
    if ema and ckpt.get('ema'):
        ema.ema.load_state_dict(ckpt['ema'].float().state_dict())  # EMA
        ema.updates = ckpt['updates']
    if resume:
        assert start_epoch > 0, f'training to {epochs} epochs is finished, nothing to resume.\n' \
                                f"Start a new training without --resume, i.e. 'python train.py --weights'"
    if epochs < start_epoch:
        epochs += ckpt['epoch']  # finetune additional epochs
    return best_fitness, start_epoch, epochs


def load_model(weight, is_val=True):
    ckpt = torch.load(weight, map_location='cpu')  # load
    if is_val:
        model = (ckpt.get('ema') or ckpt['model']).float()  # FP32 model
    else:
        model = (ckpt.get('model') or ckpt['ema']).float()  # FP32 model
    # model.load_state_dict(csd, strict=False)  # load
    return model, ckpt


class Trainable:

    def __init__(self, bs, nbs=None, gradient_clip_val=10.0) -> None:
        self.pbar = None
        self.ema = None
        self.last_opt_step = -1
        self.bs = bs
        self.train_size = None
        self.gradient_clip_val = gradient_clip_val
        if nbs is not None:
            self.accumulate = max(round(nbs / bs), 1)
        else:
            self.accumulate = 1


    def on_pretrain_routine_start(self, model, verbose=True):
        from aicmder.benchmark.torch_bench import model_info
        if RANK in {-1, 0}:
            model_info(model, verbose=verbose)

    def on_train_start(self, model, device, evaluate_func=None, patience=30, use_ema=False):
        cuda = device.type != 'cpu'
        if cuda and RANK == -1 and torch.cuda.device_count() > 1:
            with DPModel(model) as m:
                model = m.to(device)

        with DDPModel(model, auto_clean=False, devices=device) as ddp_model:
            model, device = ddp_model
            amp = check_amp(model)
            scaler = torch.cuda.amp.GradScaler(enabled=amp)   
            self.ema = None
            if use_ema:     
                try:
                    # EMA
                    self.ema = ModelEMA(model) if RANK in {-1, 0} else None
                except:
                    pass

            if evaluate_func is not None:
                self.stopper = EarlyStopping(evaluate_func, patience=patience)
            return model, device, amp, scaler, self.ema

    def on_train_epoch_start(self, model, epoch, loader, verbose=True):
        model.train()
        if RANK != -1:
            loader.sampler.set_epoch(epoch)

        pbar = enumerate(loader)
        if verbose:
            if RANK in {-1, 0}:
                nb = len(loader)  # number of batches
                # progress bar
                pbar = tqdm(pbar, total=nb,
                            bar_format='{l_bar}{bar:10}{r_bar}{bar:-10b}')
        self.pbar = pbar
        if self.train_size is None:
            self.train_size = len(loader.dataset)
        return pbar, self.train_size

    def on_train_batch_end(self, model, scaler, optimizer, loss, desc='', ni=None):
        # old--------
        # loss.backward()
        # old--------

        ############### Backward first
        scaler.scale(loss).backward()

        if ni is None or (ni is not None and ni - self.last_opt_step >= self.accumulate):
            # Only update weights every other accumulate iterations
            scaler.unscale_(optimizer)  # unscale gradients
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=self.gradient_clip_val)  # clip gradients
            scaler.step(optimizer)  # optimizer.step
            scaler.update()
            # Set gradients to None (e.g., model.zero_grad(set_to_none=True) ) before the optimizer updates the weights
            optimizer.zero_grad(set_to_none=True)
            if self.ema is not None:
                self.ema.update(model)
            if ni is not None:
                self.last_opt_step = ni
            
        # old--------
        # optimizer.step()
        # old--------
        # optimizer.zero_grad()

        if RANK in {-1, 0}:
            if self.pbar is not None:
                self.pbar.set_description(desc)


    def on_train_epoch_end(self, epoch, fi, scheduler=None):
        if scheduler is not None:
            scheduler.step()
        stop = False
        if hasattr(self, 'stopper'):
            stop = self.stopper(epoch=epoch, fitness=fi)  # early stop check
            # EarlyStopping
            if RANK != -1:  # if DDP training
                broadcast_list = [stop if RANK == 0 else None]
                dist.broadcast_object_list(broadcast_list, 0)  # broadcast 'stop' to all ranks
                if RANK != 0:
                    stop = broadcast_list[0]
        return stop
    

    def on_train_end(self):
        if WORLD_SIZE > 1 and RANK == 0:
            dist.destroy_process_group()

    def on_model_save(self, model, epoch, optimizer, best_fitness, dirname, save_state_dict_only=False):
        if RANK in {-1, 0}:
            if save_state_dict_only: 
                state_dict = model.state_dict()
            else:
                state_dict = deepcopy(de_parallel(model)).half()
            
            ckpt = {
                'epoch': epoch,
                'best_fitness': best_fitness,
                # 'model': deepcopy(de_parallel(model)).half(),
                'model': state_dict,
                'optimizer': optimizer.state_dict(),
                # 'opt': vars(opt),
                # 'wandb_id': None,  # loggers.wandb.wandb_run.id if loggers.wandb else None,
                'date': datetime.now().isoformat()}
            if self.ema is not None:
                ckpt['ema'] = deepcopy(self.ema.ema).half()
                ckpt['updates'] = self.ema.updates

            if os.path.isdir(dirname):
                save_dir = Path(dirname)
                w = save_dir / 'train'  # weights dir
                w.mkdir(parents=True, exist_ok=True)  # make dir
                best_pt = w / 'best.pt'
            else:
                best_pt = dirname
                save_dir = Path(os.path.dirname(best_pt))
                save_dir.mkdir(parents=True, exist_ok=True)  # make dir
            torch.save(ckpt, best_pt)
            del ckpt


# https://pytorch.org/tutorials/beginner/dist_overview.html
# python -m torch.distributed.run --nproc_per_node 2 /home/faith/old_f/aicmder/aicmder/torch/dist_model.py
# 2 0 0
# True
# 2 1 1
# True

def evaluate_func(fitness, best_fitness):
    best_train_acc, best_train_loss = best_fitness
    train_acc, train_loss = fitness
    if train_acc > best_train_acc or (train_acc == best_train_acc and best_train_loss is not None and train_loss < best_train_loss):
        return True
    else: 
        return False
     

if __name__ == "__main__":
    
    stopper = EarlyStopping(evaluate_func)
    stopper(10, (70, 100))
    stopper(60, (90, 100))
    stopper(80, (90, 80))
    stopper(380, (90, 70))
    print(stopper.best_epoch, stopper.best_fitness)