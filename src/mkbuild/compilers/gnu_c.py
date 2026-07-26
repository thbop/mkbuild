from dataclasses import dataclass

from mkbuild.compiler import Compiler
from mkbuild.context import Context
from mkbuild.utils import run, run_silent


@dataclass
class GNU_C(Compiler):
    """An abstract dataclass to describe some of the features of GCC."""

    COMMAND = "gcc"

    SOURCE_EXTENSION = ".c"
    TARGET_EXTENSION = ".o"

    def preprocess(self, source: str) -> bytes:
        """Preprocess for GCC."""
        result = run_silent(self.COMMAND, "-E", self.DEBUG_FLAGS.get(), source)
        return result.stdout

    def transform(self, ctx: Context, source: str, target: str) -> None:
        """Performs a basic GCC compilation."""
        flags = self.RELEASE_FLAGS if ctx.IS_RELEASE else self.DEBUG_FLAGS
        run(
            self.COMMAND,
            "-c",
            flags.get(),
            "-o",
            target,
        )
