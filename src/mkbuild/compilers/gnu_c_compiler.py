from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from mkbuild.compiler import Compiler
from mkbuild.context import Context
from mkbuild.flags import Flags
from mkbuild.utils import run, run_silent

if TYPE_CHECKING:
    from mkbuild.transformer import AcceptType


@dataclass(frozen=True)
class GNUCCompiler(Compiler):
    """An abstract dataclass to describe some of the features of GCC."""

    CTX: Context = field(default_factory=Context)
    COMMAND: str = "gcc"

    SOURCE_EXTENSION: str = ".c"
    TARGET_EXTENSION: str = ".o"

    ACCEPT: AcceptType = "previous-changed"

    FLAGS: Flags = Flags("-std=c23 -Wall -Iinclude")
    DEBUG_FLAGS: Flags = Flags("-g")
    RELEASE_FLAGS: Flags = Flags("-O2")

    def preprocess(self, source: str) -> bytes:
        """Preprocess for GCC."""
        result = run_silent(
            self.COMMAND, "-E", self._merge_flags(is_release=False), source
        )
        return str(result.stdout).encode()

    def transform(self, source: str, target: str) -> None:
        """Performs a basic GCC compilation."""
        run(
            self.COMMAND,
            "-c",
            source,
            self._merge_flags(self.CTX.IS_RELEASE),
            "-o",
            target,
        )
