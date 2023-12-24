import gc
from functools import partial
from typing import (
    Dict,
    Iterable,
    NamedTuple,
    Union,
)

import dill as pickle
import torch
import torch.distributed as dist
import tree


InnerType = (int, float, bool, str)
Tree = Union[Dict, Iterable, torch.Tensor]

"""
src & dst in this file means the `global rank` of 
the tensor i.e. the result of torch.distributed.get_rank()
"""


class PipeMeta(NamedTuple):  # utils for pipeline parallelism
    first_rank: int
    last_rank: int
    group_size: int
    prev_stage: int
    next_stage: int
    group: dist.ProcessGroup
    is_first_stage: bool
    is_middle_stage: bool
    is_last_stage: bool
    my_rank: int

    @classmethod
    def from_mpu(cls, mpu):
        group = mpu.get_pipe_parallel_group()
        group_size = mpu.get_pipe_parallel_world_size()
        my_rank = mpu.get_pipe_parallel_rank()
        first_rank = dist.get_global_rank(group, 0)
        last_rank = dist.get_global_rank(group, group_size - 1)
        prev_stage = dist.get_global_rank(group, my_rank - 1) if my_rank > 0 else None
        next_stage = (
            dist.get_global_rank(group, my_rank + 1)
            if my_rank < group_size - 1
            else None
        )
        is_first_stage = my_rank == 0
        is_middle_stage = 0 < my_rank < group_size - 1
        is_last_stage = my_rank == group_size - 1
        return cls(
            first_rank,
            last_rank,
            group_size,
            prev_stage,
            next_stage,
            group,
            is_first_stage,
            is_middle_stage,
            is_last_stage,
            my_rank,
        )


class MetaInfo:
    def __init__(self, shape, dtype):
        self.shape = shape
        self.dtype = dtype

    def get_info(self):
        return self.shape, self.dtype


def get_meta_info(tensor: torch.Tensor) -> MetaInfo:
    if not isinstance(tensor, torch.Tensor):
        return tensor

    dtype = tensor.dtype
    shape = tuple(tensor.shape)
    return MetaInfo(shape, dtype)


def create_empty_tensor(meta_info):
    if not isinstance(meta_info, MetaInfo):
        return meta_info

    shape, dtype = meta_info.get_info()
    tensor = torch.empty(shape, dtype=dtype, device="cuda")
    return tensor


def send_tensor(tensor: torch.Tensor, dst: int, group: dist.ProcessGroup) -> None:
    if not isinstance(tensor, torch.Tensor):
        return
    dist.send(tensor, dst, group=group)
    return


def recv_tensor(tensor: torch.Tensor, src: int, group: dist.ProcessGroup) -> None:
    if not isinstance(tensor, torch.Tensor):
        return
    dist.recv(tensor, src, group=group)
    return


def broadcast_tensor(tensor: torch.Tensor, src: int, group: dist.ProcessGroup) -> None:
    if not isinstance(tensor, torch.Tensor):
        return
    dist.broadcast(tensor, src, group=group)
    return


def _gather_tensor_to_list(tensor, group: dist.ProcessGroup):
    world_size = dist.get_world_size(group)
    return_list = [torch.empty_like(tensor) for _ in range(world_size)]
    dist.all_gather(return_list, tensor, group=group)
    return return_list


def gather_tensor(tensor, group: dist.ProcessGroup):
    return _gather_tensor_to_list(tensor, group)


def gather_object(obj, group=None):
    world_size = dist.get_world_size(group)
    return_list = [None] * world_size
    dist.all_gather_object(return_list, obj, group=group)
    return return_list


def send_string(string, dst, group):
    """
    string should be a byte string
    """
    encode = list(string)
    len_tensor = torch.LongTensor(data=[len(encode)]).cuda()
    dist.send(len_tensor, dst=dst, group=group)
    str_tensor = torch.LongTensor(data=encode).cuda()
    dist.send(str_tensor, dst=dst, group=group)


def recv_string(src, group):
    """
    receive a `byte` string from src
    """
    len_tensor = torch.LongTensor(data=[0]).cuda()
    dist.recv(len_tensor, src, group=group)
    str_tensor = torch.LongTensor([1] * len_tensor.item()).cuda()
    dist.recv(str_tensor, src, group=group)
    recv_str = bytes(str_tensor.tolist())
    return recv_str


def broadcast_string(string, src, group):
    """
    string should be a byte string
    """
    if dist.get_rank() == src:
        encode = list(string)
        len_tensor = torch.LongTensor(data=[len(encode)]).cuda()
        dist.broadcast(len_tensor, src=src, group=group)
        str_tensor = torch.LongTensor(data=encode).cuda()
        dist.broadcast(str_tensor, src=src, group=group)
        return string
    else:
        len_tensor = torch.LongTensor(data=[0]).cuda()
        dist.broadcast(len_tensor, src, group=group)
        str_tensor = torch.LongTensor([1] * len_tensor.item()).cuda()
        dist.broadcast(str_tensor, src, group=group)
        recv_str = bytes(str_tensor.tolist())
        return recv_str


def broadcast_tree(t: Tree, src: int, group: dist.ProcessGroup) -> None:
    if dist.get_rank() == src:
        meta_tree = tree.map_structure(get_meta_info, t)
        meta_tree_str = pickle.dumps(meta_tree)
        broadcast_string(meta_tree_str, src, group)
        p_send_tensor = partial(broadcast_tensor, src=src, group=group)
        tree.map_structure(p_send_tensor, t)
        return t

    else:
        meta_tree_str = broadcast_string(None, src, group)
        meta_tree = pickle.loads(meta_tree_str)
        t = tree.map_structure(create_empty_tensor, meta_tree)
        p_recv_tensor = partial(broadcast_tensor, src=src, group=group)
        tree.map_structure(p_recv_tensor, t)
        return t


# SEND_COUNT=0
def send_tree(t: Tree, dst: int, group: dist.ProcessGroup) -> None:
    # absl_logging.info(f"send tree from {dist.get_rank()} to {dst}")
    # global SEND_COUNT
    meta_tree = tree.map_structure(get_meta_info, t)
    # print(tree.map_structure(type, meta_tree))
    # print(tree.map_structure(lambda x:isinstance(x, Generator), meta_tree))
    # time.sleep(1)
    meta_tree_str = pickle.dumps(meta_tree)
    send_string(meta_tree_str, dst, group)
    p_send_tensor = partial(send_tensor, dst=dst, group=group)
    tree.map_structure(p_send_tensor, t)
    # SEND_COUNT+=1


# RECV_COUNT=0
def recv_tree(src: int, group: dist.ProcessGroup) -> Tree:
    # absl_logging.info(f"recv tree from {src} to {dist.get_rank()}")
    # global RECV_COUNT
    meta_tree_str = recv_string(src, group)
    meta_tree = pickle.loads(meta_tree_str)
    t = tree.map_structure(create_empty_tensor, meta_tree)
    p_recv_tensor = partial(recv_tensor, src=src, group=group)
    tree.map_structure(p_recv_tensor, t)
    # RECV_COUNT+=1
    return t


# def get_count():
#     absl_logging.info(f"recv: {RECV_COUNT},send: {SEND_COUNT}, rank:{dist.get_rank()}")
#     return RECV_COUNT,SEND_COUNT


def repr_tree(t: Tree):
    def _repr(x):
        if isinstance(x, torch.Tensor):
            if x.grad is not None:
                grad = True
            else:
                grad = False
            return [tuple(x.shape), x.dtype, grad, x.requires_grad]
        else:
            return x

    return tree.map_structure(_repr, t)


def tree_contiguous(t: Tree, to_cuda: bool = True):
    def _contiguous(tensor):
        if tensor is None or isinstance(tensor, InnerType):
            return tensor
        tensor = tensor.contiguous()
        if to_cuda:
            tensor = tensor.cuda()
        return tensor

    return tree.map_structure(_contiguous, t)
