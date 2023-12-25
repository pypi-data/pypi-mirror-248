import pickle
from copy import deepcopy
from thop import profile
import torch
import pickle
import os
from aicmder.utils.general import try_except
import gc
import datetime
import inspect

import numpy as np

dtype_memory_size_dict = {
    torch.float64: 64/8,
    torch.double: 64/8,
    torch.float32: 32/8,
    torch.float: 32/8,
    torch.float16: 16/8,
    torch.half: 16/8,
    torch.int64: 64/8,
    torch.long: 64/8,
    torch.int32: 32/8,
    torch.int: 32/8,
    torch.int16: 16/8,
    torch.short: 16/6,
    torch.uint8: 8/8,
    torch.int8: 8/8,
}
# compatibility of torch1.0
if getattr(torch, "bfloat16", None) is not None:
    dtype_memory_size_dict[torch.bfloat16] = 16/8
if getattr(torch, "bool", None) is not None:
    dtype_memory_size_dict[torch.bool] = 8/8  # pytorch use 1 byte for a bool, see https://github.com/pytorch/pytorch/issues/41571


def get_mem_space(x):
    try:
        ret = dtype_memory_size_dict[x]
    except KeyError:
        print(f"dtype {x} is not supported!")
    return ret


class MemTracker(object):
    """
    Class used to track pytorch memory usage
    Arguments:
        detail(bool, default True): whether the function shows the detail gpu memory usage
        path(str): where to save log file
        verbose(bool, default False): whether show the trivial exception
        device(int): GPU number, default is 0
    """

    def __init__(self, detail=True, path='', verbose=False, device=0):
        self.print_detail = detail
        self.last_tensor_sizes = set()
        self.gpu_profile_fn = path + f'{datetime.datetime.now():%d-%b-%y-%H:%M:%S}-gpu_mem_track.txt'
        self.verbose = verbose
        self.begin = True
        self.device = device

    def get_tensors(self):
        for obj in gc.get_objects():
            try:
                if torch.is_tensor(obj) or (hasattr(obj, 'data') and torch.is_tensor(obj.data)):
                    tensor = obj
                else:
                    continue
                if tensor.is_cuda:
                    yield tensor
            except Exception as e:
                if self.verbose:
                    print('A trivial exception occured: {}'.format(e))

    def get_tensor_usage(self):
        sizes = [np.prod(np.array(tensor.size())) * get_mem_space(tensor.dtype) for tensor in self.get_tensors()]
        return np.sum(sizes) / 1024**2

    def get_allocate_usage(self):
        return torch.cuda.memory_allocated() / 1024**2

    def clear_cache(self):
        gc.collect()
        torch.cuda.empty_cache()

    def print_all_gpu_tensor(self, file=None):
        for x in self.get_tensors():
            print(x.size(), x.dtype, np.prod(np.array(x.size()))*get_mem_space(x.dtype)/1024**2, file=file)

    def track(self):
        """
        Track the GPU memory usage
        """
        frameinfo = inspect.stack()[1]
        where_str = frameinfo.filename + ' line ' + str(frameinfo.lineno) + ': ' + frameinfo.function

        with open(self.gpu_profile_fn, 'a+') as f:

            if self.begin:
                f.write(f"GPU Memory Track | {datetime.datetime.now():%d-%b-%y-%H:%M:%S} |"
                        f" Total Tensor Used Memory:{self.get_tensor_usage():<7.1f}Mb"
                        f" Total Allocated Memory:{self.get_allocate_usage():<7.1f}Mb\n\n")
                self.begin = False

            if self.print_detail is True:
                ts_list = [(tensor.size(), tensor.dtype) for tensor in self.get_tensors()]
                new_tensor_sizes = {(type(x),
                                     tuple(x.size()),
                                     ts_list.count((x.size(), x.dtype)),
                                     np.prod(np.array(x.size()))*get_mem_space(x.dtype)/1024**2,
                                     x.dtype) for x in self.get_tensors()}
                for t, s, n, m, data_type in new_tensor_sizes - self.last_tensor_sizes:
                    f.write(f'+ | {str(n)} * Size:{str(s):<20} | Memory: {str(m*n)[:6]} M | {str(t):<20} | {data_type}\n')
                for t, s, n, m, data_type in self.last_tensor_sizes - new_tensor_sizes:
                    f.write(f'- | {str(n)} * Size:{str(s):<20} | Memory: {str(m*n)[:6]} M | {str(t):<20} | {data_type}\n')

                self.last_tensor_sizes = new_tensor_sizes

            f.write(f"\nAt {where_str:<50}"
                    f" Total Tensor Used Memory:{self.get_tensor_usage():<7.1f}Mb"
                    f" Total Allocated Memory:{self.get_allocate_usage():<7.1f}Mb\n\n")


def torch_info():
    print('Pytorch version\t:', torch.__version__)
    print('CUDA version\t:', torch.version.cuda)
    # 获取CUDNN版本号
    cudnn_version = torch.backends.cudnn.version()
    print("CUDNN version\t:", cudnn_version)
    print('GPU\t\t:', torch.cuda.get_device_name())
    print('GPU count:', torch.cuda.device_count())


def save_batch(batch, filename="batch.pkl"):
    with open(filename, 'wb') as outp:
        pickle.dump(batch, outp, pickle.HIGHEST_PROTOCOL)


@try_except
def model_info(model, pickle_path="batch.pkl", verbose=False, use_pretty=True, input_shape=None, need_profile=True):

    n_p = sum(x.numel() for x in model.parameters())  # number parameters
    n_g = sum(x.numel() for x in model.parameters() if x.requires_grad)  # number gradients
    model_input = None
    if verbose:

        if use_pretty:
            import importlib
            spam_loader = importlib.find_loader('prettytable')
            found = spam_loader is not None
            if found:
                from prettytable import PrettyTable
        else:
            found = False
        
        table = []
        if found:
            if hasattr(model, "_get_name"):
                model_name = model._get_name()
                table.append([' ', '  ',  '   ', model_name, '    ', '     ', '      '])

            table.append(['layer', 'name', 'gradient', 'parameters', 'shape', 'mu', 'sigma'])
        else:
            table.append(f"{'layer':>5} {'name':>40} {'gradient':>9} {'parameters':>12} {'shape':>20} {'mu':>10} {'sigma':>10}")
        
        # for replace model
        # for i, (name, layer) in enumerate(model.named_modules()):
        #     if isinstance(layer, nn.ReLU):  
        #         
        for i, (name, p) in enumerate(model.named_parameters()):
            name = name.replace('module_list.', '')
            if found:
                table.append([i, name, p.requires_grad, p.numel(), list(p.shape),'%.3g' % p.mean().item(), '%.3g' % p.std().item()])
                
            else:
                table.append('%5g %40s %9s %12g %20s %10.3g %10.3g' % (i, name, p.requires_grad, p.numel(), list(p.shape), p.mean(), p.std()))
        if not found:
            for item in table:
                print(item)
        else:
            tab = PrettyTable(table[0], align='r', valign='t')
            tab.add_rows(table[1:])
            print(tab)

    fs = ''
    if need_profile:
        try:
            if pickle_path is not None and os.path.exists(pickle_path):
                with open(pickle_path, 'rb') as inp:
                    model_input = pickle.load(inp)
                    if isinstance(model_input, list):
                        model_input = [data.to(next(model.parameters()).device) for data in model_input]
                    else:
                        model_input.to(next(model.parameters()).device)
            else:
                first_parameter = next(model.parameters())
                if input_shape is None:
                    input_shape = first_parameter.size()
                model_input = torch.zeros(input_shape, device=next(model.parameters()).device).contiguous()  # input
            copy_model = deepcopy(model)
            if isinstance(model_input, list):
                flops = profile(copy_model, inputs=model_input, verbose=False)[0] / 1E9 * 2
            else:
                flops = profile(copy_model, inputs=(model_input,), verbose=False)[0] / 1E9 * 2
            fs = ', %.1f GFLOPs' % (flops)
            copy_model = copy_model.cpu()
            del copy_model
        except Exception as e:
            print(e)
            fs = ''

    print(f"summary: {len(list(model.modules()))} layers, {n_p} parameters, {n_g} gradients{fs}")
    return model_input
