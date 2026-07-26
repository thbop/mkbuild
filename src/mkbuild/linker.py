from dataclasses import dataclass

from mkbuild.transformer import Transformer


@dataclass
class Linker(Transformer):
    """A dataclass to describe a linker."""

    pass
