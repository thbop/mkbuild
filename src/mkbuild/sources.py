import os
from pathlib import Path
from typing import TYPE_CHECKING, Iterator

from mkbuild.linker import Linker
from mkbuild.transformer import Transformer

if TYPE_CHECKING:
    pass


class Sources:
    """A source collection associated with a compiler or linker."""

    def __init__(
        self,
        transformer: Transformer | Linker,
        sources: list[str] | None = None,
    ) -> None:
        self.transformer = transformer
        self._sources: list[str] = (
            [
                filename
                for filename in sources
                if self._has_valid_source_extension(filename)
            ]
            if sources is not None
            else self._read_sources()
        )

    def copywith(self, sources: list[str]) -> Sources:
        """Creates a copy of an existing Sources object but with new sources."""
        return Sources(self.transformer, sources)

    @property
    def sources(self) -> Iterator[str]:
        """Iterator wrapper for sources."""
        return self._sources.__iter__()

    @property
    def targets(self) -> Iterator[str]:
        """Iterator wrapper for targets."""
        return [
            self._get_source_as_target(src) for src in self.sources
        ].__iter__()

    @property
    def is_empty(self) -> bool:
        """Returns true if the source collection is empty."""
        return len(self._sources) == 0

    def _has_valid_source_extension(self, src: str) -> bool:
        """Checks if a file path has the transformer source extension."""
        return Path(src).suffix == self.transformer.SOURCE_EXTENSION

    def _get_source_as_target(self, src: str) -> str:
        """Replaces a source file extension with the target extension."""
        identifier = (
            str(Path(src).with_suffix(self.transformer.TARGET_EXTENSION))
            .replace("\\", ".")
            .replace("/", ".")
        )
        return str(
            Path(
                self.transformer.CTX.BIN_PATH,
                ".".join(identifier.split(".")[1:]),
            )
        )

    def _read_sources(self) -> list[str]:
        """Walks through the `ctx.SRC_PATH` and collects all sources."""
        sources: list[str] = []
        for root, _, files in os.walk(self.transformer.CTX.SRC_PATH):
            sources += [
                str(Path(root, filename))
                for filename in files
                if self._has_valid_source_extension(filename)
            ]
        return sources
