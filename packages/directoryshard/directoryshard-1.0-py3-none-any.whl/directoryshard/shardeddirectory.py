from __future__ import annotations

from pathlib import Path

from directoryshard import sharded


class ShardedDirectory:
    """"return sharded paths from specfied directory"""

    def __init__(self,root:str | Path)->None:
        """Shard files at this directory
        :param root: absolute path of the directory
        """
        self.root = Path(root)
        if self.root.is_absolute():
            return
        raise ValueError(f"{root} must be absolute")


    def filepath(self,file: str| Path)->Path:
        """Sharded path of file"""
        return self.root.joinpath(sharded(file))
