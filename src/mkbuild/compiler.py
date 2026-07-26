from dataclasses import dataclass

from mkbuild.transformer import Transformer


@dataclass
class Compiler(Transformer):
    """A dataclass to handle a compiler."""

    pass
