import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

from mkbuild.linker import Linker
from mkbuild.transformer import Transformer

if TYPE_CHECKING:
    from mkbuild.context import Context


class Sources:
    """A source collection associated with a compiler or linker."""

    def __init__(
        self,
        ctx: Context,
        transformer: Transformer | Linker,
        sources: list[str] | None = None,
    ) -> None:
        self.ctx = ctx
        self.transformer = transformer
        self._sources: list[str] = (
            [
                filename
                for filename in sources
                if self._has_valid_source_extension(filename)
            ]
            if sources
            else self._read_sources()
        )

    def copywith(self, sources: list[str]) -> Sources:
        """Creates a copy of an existing Sources object but with new sources."""
        return Sources(self.ctx, self.transformer, sources)

    @property
    def sources(self) -> Iterator[str]:
        """Iterator wrapper for sources."""
        return self._sources.__iter__()

    @property
    def targets(self) -> Iterator[str]:
        """Iterator wrapper for targets."""
        return [
            self._get_source_with_target_extension(src) for src in self.sources
        ].__iter__()

    def _has_valid_source_extension(self, src: str) -> bool:
        """Checks if a file path has the transformer source extension."""
        return Path(src).suffix == self.transformer.SOURCE_EXTENSION

    def _get_source_with_target_extension(self, src: str) -> str:
        """Replaces a source file extension with the target extension."""
        return str(Path(src).with_suffix(self.transformer.TARGET_EXTENSION))

    def _read_sources(self) -> list[str]:
        """Walks through the `ctx.SRC_PATH` and collects all sources."""
        sources: list[str] = []
        for root, _, files in os.walk(self.ctx.SRC_PATH):
            sources += [
                str(Path(root, filename))
                for filename in files
                if self._has_valid_source_extension(filename)
            ]

        return sources
