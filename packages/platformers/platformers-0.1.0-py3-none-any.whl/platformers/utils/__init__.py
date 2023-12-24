import gc
import logging
import torch
from .parallel import init_parallel, gather_object
import os
from pathlib import Path
import datasets
import json

PATH = Path(os.environ.get("HF_HOME", "~/.cache/huggingface"))

# %%


def release_cuda():
    gc.collect()
    torch.cuda.empty_cache()
    gc.collect()


def move_engine(engine, dst="cpu"):
    # not support zero3 now, but not hard
    try:
        import tree
    except ImportError:
        raise ImportError("Please install dm-tree by `pip install dm-tree` first")
    sd = engine.optimizer.state_dict()
    release_cuda()
    gc.disable()
    _OBJs = [t for t in gc.get_objects() if isinstance(t, torch.Tensor)]

    def move_tensor_cpu(x):
        if isinstance(x, torch.Tensor):
            storage = x.storage()
            for obj in _OBJs:
                if obj.storage()._cdata == storage._cdata:
                    obj.data = obj.data.to(dst)
            x.data = x.data.to(dst)

            if x.requires_grad:
                if isinstance(x.grad, torch.Tensor):
                    x.grad.data = x.grad.data.to(dst)

    tree.map_structure(move_tensor_cpu, sd)
    gc.enable()
    release_cuda()


def load_dataset(path, *args, **kwargs):
    logging.info(f"Loading {path}")
    try:
        return datasets.load_dataset(path, *args, **kwargs)
    except Exception as e:
        logging.error(e)
        if "/" in path:
            hf_user, hf_repo = path.split("/")
            cache_name = f"{hf_user}___{datasets.load.camelcase_to_snakecase(hf_repo)}"
        else:
            cache_name = datasets.load.camelcase_to_snakecase(path)
        cache_path = (
            datasets.config.HF_DATASETS_CACHE / cache_name / "default" / "0.0.0"
        )
        hashes = [p for p in cache_path.glob("*") if p.is_dir()]
        hash = sorted(hashes, key=lambda p: p.stat().st_mtime)[-1]
        ds_info = json.load(open(hash / "dataset_info.json"))

        data_files = list(ds_info["download_checksums"].keys())
        splits = {}
        for split in ds_info["splits"].keys():
            splits[split] = [p for p in data_files if Path(p).name.startswith(split)]
        return datasets.load_dataset(
            ds_info["builder_name"], data_files=splits, **kwargs
        )
