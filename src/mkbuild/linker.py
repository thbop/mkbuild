from dataclasses import dataclass

from mkbuild.transformer import Transformer


@dataclass(frozen=True, kw_only=True)
class Linker(Transformer[list[str], None]):
    """A dataclass to describe a linker."""

    TARGET: str
