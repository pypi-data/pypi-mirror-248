# coding:utf-8
import sys

__version__ = '0.5.9'

# from aicmder.utils import utils
# sys.modules['aicmder.common.utils'] = utils
from aicmder.commands import *

# torch
from aicmder.torch import select_device, CudaDecorators, cpu, gpu, try_gpu, train_params, HyperParameters

# util
from aicmder.utils import WorkingDirectory, try_except, threaded, iSummaryWriter, FileMonitor

# benchmark
from aicmder.benchmark import model_info, torch_info

# module
from aicmder.module.module import Module
from aicmder.module.define import ModuleDefine
from aicmder.module.module import serving, runnable

# serving
from aicmder.service.worker import Worker
try:
    from aicmder.service.http_service import HTTPProxy
except Exception as e:
    print(e)
from aicmder.service.server import ServerQueue


from aicmder.service.PPworker import PPworker

# common
import aicmder.common as Common

try:
    from aicmder.service.http_service import Client
except Exception as e:
    print(e)


import sys
import os


def import_parent(current_file):
    # getting the name of the directory
    # where the this file is present.
    current = os.path.dirname(os.path.realpath(current_file))

    # Getting the parent directory name
    # where the current directory is present.
    parent = os.path.dirname(current)

    # adding the parent directory to
    # the sys.path.
    sys.path.append(parent)
    # print(parent, __file__)



def add_to_class(Class):
    """Defined in :numref:`sec_oo-design`"""
    def wrapper(obj):
        setattr(Class, obj.__name__, obj)
    return wrapper

from aicmder.utils import AttrDict
