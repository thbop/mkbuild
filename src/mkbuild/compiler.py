from dataclasses import dataclass

from mkbuild.transformer import Transformer


@dataclass(frozen=True)
class Compiler(Transformer[str, str]):
    """A dataclass to handle a compiler."""
