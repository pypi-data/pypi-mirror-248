import deepspeed
import torch
from optimus import mpu, fused_kernels
from deepspeed.runtime.pipe.topology import PipeModelDataParallelTopology
from accelerate.utils import set_seed
import torch.distributed as dist
import os


def init_parallel(
    mp_size,
    pp_size=1,
    rank_divide=None,
    seed=42,
    mpu=mpu,
    load_fused_kernels=True,
    port=None,
    name=None,
    with_cuda=True,
):
    if not with_cuda:
        backend = "mpi"
    else:
        backend = "nccl"
    if port is not None:
        # only use in one node, multi-node obey torchrun env set
        deepspeed.init_distributed(
            dist_backend=backend,
            init_method="env://",
            verbose=False,
            distributed_port=port,
        )
    else:
        deepspeed.init_distributed(
            dist_backend=backend,
            init_method="env://",
            verbose=False,
        )
    topo = PipeModelDataParallelTopology(
        num_pp=pp_size,
        num_mp=mp_size,
        num_dp=dist.get_world_size() // mp_size // pp_size,
    )
    mpu.initialize_model_parallel(mp_size, topo, model_name=name)
    if not with_cuda:
        return topo

    if rank_divide is None:
        rank_divide = dist.get_world_size()
    try:
        device_rank = int(os.environ["LOCAL_RANK"])
    except Exception:
        rank = dist.get_rank()
        device_rank = rank % rank_divide  # convieniently, for single & multi-node
    torch.cuda.set_device(device_rank)
    # note that this function will set the seed for all processes with same seed
    set_seed(seed)
    deepspeed.checkpointing.configure(mpu)
    mpu.model_parallel_cuda_manual_seed(seed)
    if load_fused_kernels:
        fused_kernels.load_fused_kernels()
    # dist.GroupMember.WORLD.barrier()
    return topo


def gather_object(obj, group=None):
    world_size = dist.get_world_size(group)
    return_list = [None] * world_size
    dist.all_gather_object(return_list, obj, group=group)
    return return_list
