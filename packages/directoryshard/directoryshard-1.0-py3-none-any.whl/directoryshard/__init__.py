from __future__ import annotations

import base64
import hashlib
import importlib.metadata
import logging
from pathlib import Path

directoryshard_logger = logging.getLogger(__name__)

__version__ = importlib.metadata.version('directoryshard')


def shardprefix(filename: str) -> str:
    """Return a 2 character alphanumeric string by deterministically hashing filename"""
    return base64.b32encode(hashlib.md5(filename.encode()).digest()).decode().lower()[:2]


def sharded(file: str | Path) -> Path:
    """Return path sharded into subdirectory"""
    p = file if isinstance(file,Path) else Path(file)
    return p.parent / shardprefix(p.stem) / p.stem

from directoryshard.shardeddirectory import ShardedDirectory
