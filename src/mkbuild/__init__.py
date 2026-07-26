import os

from .compiler import Compiler
from .context import Context
from .flags import Flags, OSFlags
from .linker import Linker
from .sources import Sources
from .utils import run, run_silent

env = os.environ.copy()
env["FORCE_COLOR"] = "1"

__all__ = [
    "Compiler",
    "Linker",
    "Context",
    "Flags",
    "OSFlags",
    "Sources",
    "run",
    "run_silent",
]
