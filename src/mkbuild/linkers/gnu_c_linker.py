from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING

from mkbuild.context import Context
from mkbuild.flags import Flags
from mkbuild.linker import Linker
from mkbuild.utils import run

if TYPE_CHECKING:
    from mkbuild.transformer import AcceptType


@dataclass(frozen=True)
class GNUCLinker(Linker):
    """An abstract dataclass to describe the GNU C Linker."""

    CTX: Context = field(
        default_factory=lambda: Context(SRC_PATH="bin", BIN_PATH="bin")
    )
    COMMAND: str = "gcc"

    ACCEPT: AcceptType = "all"

    SOURCE_EXTENSION: str = ".o"

    FLAGS: Flags = Flags("-Wall -Llib")
    DEBUG_FLAGS: Flags = Flags("-g")
    RELEASE_FLAGS: Flags = Flags("-O2")

    def transform(self, source: list[str], target: None) -> None:
        """Performs a basic GCC linkage.

        Args:
            ctx: The context
            source: The concatenated sources to link
            target: The target executable file
        """
        target_path = str(
            Path(self.CTX.BIN_PATH, self.TARGET + self.TARGET_EXTENSION)
        )
        run(
            self.COMMAND,
            " ".join(source),
            self._merge_flags(self.CTX.IS_RELEASE),
            "-o",
            target_path,
        )
