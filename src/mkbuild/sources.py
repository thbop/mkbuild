import os
from pathlib import Path
from typing import Iterator

from mkbuild.compiler import Compiler
from mkbuild.context import Context
from mkbuild.linker import Linker


class Sources:
    """A source collection associated with a compiler or linker."""

    def __init__(
        self,
        ctx: Context,
        collector: Compiler | Linker,
        sources: list[str] | None = None,
    ):
        self.ctx = ctx
        self.collector = collector
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
        return Sources(self.ctx, self.collector, sources)

    def __iter__(self) -> Iterator[str]:
        """Iterator wrapper for internal list."""
        return self._sources.__iter__()

    def _has_valid_source_extension(self, filename: str) -> bool:
        """Checks if a file path has the collector source extension."""
        return Path(filename).suffix == self.collector.SOURCE_EXTENSION

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
