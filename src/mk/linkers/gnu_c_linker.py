from dataclasses import dataclass

from mk.context import Context
from mk.flags import Flags
from mk.linker import Linker
from mk.utils import run


@dataclass(frozen=True)
class GNUCLinker(Linker):
    """An abstract dataclass to describe the GNU C Linker."""

    COMMAND: str = "gcc"

    SOURCE_EXTENSION: str = ".o"

    FLAGS: Flags = Flags("-Wall -Llib")
    DEBUG_FLAGS: Flags = Flags("-g")
    RELEASE_FLAGS: Flags = Flags("-O2")

    def transform(self, ctx: Context, source: list[str], target: None) -> None:
        """Performs a basic GCC linkage.

        Args:
            ctx: The context
            source: The concatenated sources to link
            target: The target executable file
        """
        run(
            self.COMMAND,
            "-c",
            " ".join(source),
            self._merge_flags(ctx.IS_RELEASE),
            "-o",
            self.TARGET + self.TARGET_EXTENSION,
        )
