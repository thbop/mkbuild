from abc import ABC

from mkbuild.compiler import Compiler
from mkbuild.utils import run_silent


class GNU_C(ABC, Compiler):
    """An abstract dataclass to describe some of the features of GCC."""

    COMMAND = "gcc"

    SOURCE_EXTENSION = ".c"
    TARGET_EXTENSION = ".o"

    def preprocess(self, filename) -> str:
        """Preprocess for GCC."""
        result = run_silent(self.COMMAND, "-E", self.DEBUG_FLAGS, filename)
        return result.stdout
