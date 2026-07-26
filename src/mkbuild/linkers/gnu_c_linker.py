from mkbuild.context import Context
from mkbuild.linker import Linker
from mkbuild.utils import run


class GNUCLinker(Linker):
    """An abstract dataclass to describe the GNU C Linker."""

    COMMAND = "gcc"

    SOURCE_EXTENSION = ".o"

    def transform(self, ctx: Context, source: list[str], target: None) -> None:
        """Performs a basic GCC linkage.

        Args:
            ctx: The context
            source: The concatenated sources to link
            target: The target executable file
        """
        flags = self.RELEASE_FLAGS if ctx.IS_RELEASE else self.DEBUG_FLAGS
        run(
            self.COMMAND,
            "-c",
            " ".join(source),
            flags.get(),
            "-o",
            self.TARGET + self.TARGET_EXTENSION,
        )
