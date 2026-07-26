from dataclasses import dataclass

from mk.context import Context
from mk.hash_handler import HashHandler
from mk.pipe import Pipe

from .transformer import Transformer


@dataclass(frozen=True)
class Pipeline:
    """The build pipeline."""

    TRANSFORMERS: list[Transformer]
    CONTEXT: Context = Context()

    def run(self) -> None:
        """Runs a pipeline in order."""
        hash_handler = HashHandler(self.CONTEXT)

        raw_sources: list[str] | None = None
        for transformer in self.TRANSFORMERS:
            pipe = Pipe(self.CONTEXT, hash_handler, transformer)
            raw_sources = pipe.run(raw_sources)
