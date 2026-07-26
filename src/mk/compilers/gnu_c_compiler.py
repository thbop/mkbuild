from dataclasses import dataclass

from mk.compiler import Compiler
from mk.context import Context
from mk.flags import Flags
from mk.utils import run, run_silent


@dataclass(frozen=True)
class GNUCCompiler(Compiler):
    """An abstract dataclass to describe some of the features of GCC."""

    COMMAND: str = "gcc"

    SOURCE_EXTENSION: str = ".c"
    TARGET_EXTENSION: str = ".o"

    FLAGS: Flags = Flags("-std=c23 -Wall -Iinclude")
    DEBUG_FLAGS: Flags = Flags("-g")
    RELEASE_FLAGS: Flags = Flags("-O2")

    def preprocess(self, source: str) -> bytes:
        """Preprocess for GCC."""
        result = run_silent(self.COMMAND, "-E", self.DEBUG_FLAGS.get(), source)
        return result.stdout

    def transform(self, ctx: Context, source: str, target: str) -> None:
        """Performs a basic GCC compilation."""
        run(
            self.COMMAND,
            "-c",
            source,
            self._merge_flags(ctx.IS_RELEASE),
            "-o",
            target,
        )
