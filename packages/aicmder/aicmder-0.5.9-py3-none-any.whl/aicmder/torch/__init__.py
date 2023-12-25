import torch
import torch.distributed as dist
import torch.nn as nn
import time
from torch.nn.parallel import DistributedDataParallel as DDP
import numpy as np
import random
import os
from aicmder.torch.dist_model import check_version as check_version
import inspect
import gc
import collections
try:
    from matplotlib import pyplot as plt
    from matplotlib_inline import backend_inline
    from IPython import display
except:
    pass


def freeze_parameter(model):
    for param in model.parameters():
        param.requires_grad = False


def train_params(model, verbose=False):
    params_to_update = []
    for name, param in model.named_parameters():
        if param.requires_grad == True:
            params_to_update.append(param)
            if verbose:
                print("\t", name)
    return params_to_update


# def set_seed(seed=42):
#     random.seed(seed)
#     os.environ['PYHTONHASHSEED'] = str(seed)
#     np.random.seed(seed)
#     torch.manual_seed(seed)
#     torch.cuda.manual_seed(seed)
#     torch.backends.cudnn.deterministic = True

def init_seeds(seed=0, deterministic=False):
    # Initialize random number generator (RNG) seeds https://pytorch.org/docs/stable/notes/randomness.html
    # cudnn seed 0 settings are slower and more reproducible, else faster and less reproducible
    import torch.backends.cudnn as cudnn

    if deterministic and check_version(torch.__version__, '1.12.0'):  # https://github.com/ultralytics/yolov5/pull/8213
        torch.use_deterministic_algorithms(True)
        os.environ['CUBLAS_WORKSPACE_CONFIG'] = ':4096:8'
        os.environ['PYTHONHASHSEED'] = str(seed)

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    cudnn.benchmark, cudnn.deterministic = (False, True) if seed == 0 else (True, False)
    torch.cuda.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)  # for Multi-GPU, exception safe


def time_sync():
    # PyTorch-accurate time
    if torch.cuda.is_available():
        torch.cuda.synchronize()
    return time.time()


"""
###################################################################################
add by d2l.ai
###################################################################################
"""


def cpu():
    """Defined in :numref:`sec_use_gpu`"""
    return torch.device('cpu')


def gpu(i=0):
    """Defined in :numref:`sec_use_gpu`"""
    return torch.device(f'cuda:{i}')


def num_gpus():
    """Defined in :numref:`sec_use_gpu`"""
    return torch.cuda.device_count()


def try_gpu(i=0):
    """Return gpu(i) if exists, otherwise return cpu().

    Defined in :numref:`sec_use_gpu`"""
    if num_gpus() >= i + 1:
        return gpu(i)
    return cpu()


def try_all_gpus():
    """Return all available GPUs, or [cpu(),] if no GPU exists.

    Defined in :numref:`sec_use_gpu`"""
    return [gpu(i) for i in range(num_gpus())]


class HyperParameters:
    # def save_hyperparameters(self, ignore=[]):
    #     """Defined in :numref:`sec_oo-design`"""
    #     raise NotImplemented

    def save_hyperparameters(self, ignore=[]):
        """Save function arguments into class attributes.

        Defined in :numref:`sec_utils`"""
        frame = inspect.currentframe().f_back
        _, _, _, local_vars = inspect.getargvalues(frame)
        self.hparams = {k: v for k, v in local_vars.items()
                        if k not in set(ignore+['self']) and not k.startswith('_')}
        for k, v in self.hparams.items():
            if isinstance(v, dict):
                for _k, _v in v.items():
                    try:
                        setattr(self, _k, _v)
                    except:
                        pass
            else:
                setattr(self, k, v)

class Module(nn.Module, HyperParameters):

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.save_hyperparameters()
        self.board = ProgressBoard()

    def to_gpu(self, i=0):
        self.to(gpu(i))

    def to_cpu():
        self.to(cpu())

    def try_gpu(i=0):
        self.to(try_gpu(i))

    def apply_init(self, inputs, init=None):
        """Defined in :numref:`sec_lazy_init`"""
        self.forward(*inputs)
        if init is not None:
            self.net.apply(init)

    def loss(self, y_hat, y):
        raise NotImplementedError

    def forward(self, X):
        raise NotImplementedError
        # assert hasattr(self, 'net'), 'Neural network is defined'
        # return self.net(X)


def use_svg_display():
    """Use the svg format to display a plot in Jupyter.

    Defined in :numref:`sec_calculus`"""
    backend_inline.set_matplotlib_formats('svg')


class ProgressBoard(HyperParameters):
    """Plot data points in animation.

    Defined in :numref:`sec_oo-design`"""

    def __init__(self, xlabel=None, ylabel=None, xlim=None,
                 ylim=None, xscale='linear', yscale='linear',
                 ls=['-', '--', '-.', ':'], colors=['C0', 'C1', 'C2', 'C3'],
                 fig=None, axes=None, figsize=(3.5, 2.5), display=True, is_save=False, save_name="plot.png"):
        self.save_hyperparameters()

    # def draw(self, x, y, label, every_n=1):
    #     raise NotImplemented

    def draw(self, x, y, label, every_n=1):
        """Defined in :numref:`sec_utils`"""
        Point = collections.namedtuple('Point', ['x', 'y'])
        if not hasattr(self, 'raw_points'):
            self.raw_points = collections.OrderedDict()
            self.data = collections.OrderedDict()
        if label not in self.raw_points:
            self.raw_points[label] = []
            self.data[label] = []
        points = self.raw_points[label]
        line = self.data[label]
        points.append(Point(x, y))
        if len(points) != every_n:
            return

        def mean(x): return sum(x) / len(x)
        line.append(Point(mean([p.x for p in points]),
                          mean([p.y for p in points])))
        points.clear()
        if not self.display:
            return
        use_svg_display()
        if self.fig is None:
            self.fig = plt.figure(figsize=self.figsize)
        plt_lines, labels = [], []
        for (k, v), ls, color in zip(self.data.items(), self.ls, self.colors):
            plt_lines.append(plt.plot([p.x for p in v], [p.y for p in v],
                                      linestyle=ls, color=color)[0])
            labels.append(k)
        axes = self.axes if self.axes else plt.gca()
        if self.xlim:
            axes.set_xlim(self.xlim)
        if self.ylim:
            axes.set_ylim(self.ylim)
        if not self.xlabel:
            self.xlabel = self.x
        axes.set_xlabel(self.xlabel)
        axes.set_ylabel(self.ylabel)
        axes.set_xscale(self.xscale)
        axes.set_yscale(self.yscale)
        axes.legend(plt_lines, labels)
        display.display(self.fig)
        if self.is_save:
            plt.savefig(self.save_name)
        display.clear_output(wait=True)


class DataModule(HyperParameters):
    """Defined in :numref:`sec_oo-design`"""

    def __init__(self, *args, **kwargs):
        self.save_hyperparameters()
        super().__init__(*args, **kwargs)

    def get_dataloader(self, train):
        raise NotImplementedError

    def train_dataloader(self):
        return self.get_dataloader(train=True)

    def val_dataloader(self):
        return self.get_dataloader(train=False)

    def get_tensorloader(self, tensors, train, indices=slice(0, None)):
        """Defined in :numref:`sec_synthetic-regression-data`"""
        tensors = tuple(a[indices] for a in tensors)
        dataset = torch.utils.data.TensorDataset(*tensors)
        return torch.utils.data.DataLoader(dataset, self.batch_size,
                                           shuffle=train)


def select_device(device='', batch_size=0):
    # device = 'cpu' or '0' or '0,1,2,3'
    device = str(device).strip().lower().replace(
        'cuda:', '')  # to string, 'cuda:0' to '0'
    cpu = device == 'cpu'
    if cpu:
        # force torch.cuda.is_available() = False
        os.environ['CUDA_VISIBLE_DEVICES'] = '-1'
    elif device:  # non-cpu device requested
        pass
        ######## comment 
        # os.environ['CUDA_VISIBLE_DEVICES'] = device  # set environment variable
        assert torch.cuda.is_available(
        ), f'CUDA unavailable, invalid device {device} requested'  # check availability

    cuda = not cpu and torch.cuda.is_available()
    if cuda:
        # range(torch.cuda.device_count())  # i.e. 0,1,6,7
        devices = device.split(',') if device else ['0']
        n = len(devices)  # device count
        if n > 1 and batch_size > 0:  # check batch_size is divisible by device_count
            assert batch_size % n == 0, f'batch-size {batch_size} not multiple of GPU count {n}'
    return torch.device('cuda:{}'.format(devices[0]) if cuda else 'cpu')


############################### add by faith (modify layer)

def hook_model(model, module_idx=-1, hook_func=None, *args, **kwargs):
    modules_dict = getattr(model, '_modules')
    modules_size = len(modules_dict)
    if module_idx == -1:
        module_idx = modules_size - 1
    for idx, module_name in enumerate(modules_dict):
        if idx == module_idx:
            if hook_func is not None:
                hook_func(modules_dict, module_name, *args, **kwargs)

def modify_last_classifier(modules_dict, module_name, out_features=10):
    '''
        call example: hook_model(model, hook_func=modify_last_classifier, out_features=10)
        # old method
        # last_classifier = list(model.classifier.children())[:-1]
        # model.classifier = torch.nn.Sequential(*last_classifier, torch.nn.Linear(4096, 10))
    '''
    classifier = modules_dict[module_name]
    if type(classifier).__name__ != 'Sequential':
        modules_dict[module_name] = torch.nn.Linear(classifier.in_features, out_features=out_features) 
    else:
        last_classifier = list(classifier.children())[:-1] 
        last_classifier_layer = list(classifier.children())[-1]  
        modules_dict[module_name] = torch.nn.Sequential(*last_classifier, torch.nn.Linear(last_classifier_layer.in_features, out_features=out_features))     


from contextlib import contextmanager
class CudaDecorators(object):
    optimize_cuda_cache = False

    @classmethod
    @contextmanager
    def empty_cuda_cache(cls):
        yield
        if cls.optimize_cuda_cache and torch.cuda.is_available():
            gc.collect()
            torch.cuda.empty_cache()
            gc.collect()


if __name__ == "__main__":
    progress = ProgressBoard(xlabel="x", ylabel="y", is_save=True)
    label = "test"
    x = np.arange(10)
    y = np.arange(10) + 100
    progress.draw(x, y, label)
