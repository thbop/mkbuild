from mkbuild.compiler import Compiler
from mkbuild.utils import run_silent


class GNU_C(Compiler):
    """An abstract class to describe some of the features of GCC."""

    @property
    def compiler(self) -> str:
        """GCC Compiler."""
        return "gcc"

    def preprocess(self, filename) -> str:
        """Preprocess for GCC."""
        result = run_silent(self.compiler, "-E", self.flags, filename)
        return result.stdout
