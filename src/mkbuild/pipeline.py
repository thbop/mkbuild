from dataclasses import dataclass

from mkbuild.context import Context
from mkbuild.pipe import Pipe
from mkbuild.utils import log

from .transformer import Transformer


@dataclass(frozen=True)
class Pipeline:
    """The build pipeline."""

    CONTEXT: Context
    TRANSFORMERS: list[Transformer]

    def run(self) -> None:
        """Runs a pipeline in order."""
        with self.CONTEXT.HASH_HANDLER as hash_handler:
            raw_sources: list[str] | None = None
            for transformer in self.TRANSFORMERS:
                pipe = Pipe(hash_handler, transformer)
                raw_sources = pipe.run(raw_sources)

        log("Done!")
