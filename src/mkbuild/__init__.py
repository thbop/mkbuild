import os
from pathlib import Path

import __main__
from mkbuild.exceptions import MKInvalidMKName

from . import compilers, linkers
from .compiler import Compiler
from .context import Context
from .flags import Flags, OSFlags
from .linker import Linker
from .pipe import Pipe
from .pipeline import Pipeline
from .sources import Sources
from .utils import run, run_silent

_mk_env = os.environ.copy()
_mk_env["FORCE_COLOR"] = "1"

_mk_main_file_path = getattr(__main__, "__file__")

if Path(_mk_main_file_path).name != "mk.py":
    raise MKInvalidMKName()

__all__ = [
    "Compiler",
    "Linker",
    "Context",
    "Flags",
    "OSFlags",
    "Pipe",
    "Pipeline",
    "Sources",
    "run",
    "run_silent",
    "compilers",
    "linkers",
]
