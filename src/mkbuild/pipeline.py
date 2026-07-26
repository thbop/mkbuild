from dataclasses import dataclass

from mkbuild.pipe import Pipe


@dataclass(frozen=True)
class Pipeline:
    """The build pipeline."""

    PIPES: list[Pipe]

    def run(self) -> None:
        """Runs a pipeline in order."""
        raw_sources: list[str] | None = None
        for pipe in self.PIPES:
            raw_sources = pipe.run(raw_sources)
