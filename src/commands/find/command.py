"""find command builder. See SYNOPSIS: find [-H] [-L] [-P] [-D debugopts] [-Olevel] [path...] [expression]."""

from pathlib import Path
from typing import Literal

from argbuilder import Command as BaseCommand, Field

# -P never, -L follow, -H follow only for command-line args
SYMLINKS_OPT: dict[str, str] = {
    "never": "P",
    "follow": "L",
    "command_line": "H",
}

# -type: b block, c character, d directory, p pipe, f file, l symlink, s socket, D door
FILE_TYPE_OPT: dict[str, str] = {
    "block": "b",
    "character": "c",
    "directory": "d",
    "pipe": "p",
    "file": "f",
    "symlink": "l",
    "socket": "s",
    "door": "D",
}

def map_symlink_option(value: str) -> str:
    return SYMLINKS_OPT[value]

def map_filetype_option(value: str) -> str:
    return FILE_TYPE_OPT[value]

type SymlinkFollowPolicy = Literal["never", "follow", "command_line"]
type Action = Literal["print", "print0", "delete"]
type FileType = Literal[
    "block", 
    "character", 
    "directory", 
    "pipe", 
    "file", 
    "symlink", 
    "socket", 
    "door"
]

class Command(BaseCommand):
    arg0 = "find"

    follow_symlinks: SymlinkFollowPolicy = Field("-{value}", map_symlink_option)
    debug: str = Field(["-D", "{value}"])
    optimization_level: int = Field(["-O", "{value}"])
    path: str | Path = Field("{value}")
    max_depth: int = Field(["-maxdepth", "{value}"])
    min_depth: int = Field(["-mindepth", "{value}"])
    depth: bool = Field("-depth")
    name: str = Field(["-name", "{value}"])
    file_type: FileType = Field(["-type", "{value}"], map_filetype_option)
    empty: bool = Field("-empty")
    action: Action = Field("-{value}")