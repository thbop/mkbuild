from abc import ABC, abstractmethod
from dataclasses import dataclass

from mkbuild.context import Context
from mkbuild.flags import Flags


@dataclass
class Transformer(ABC):
    """A dataclass that describes the properties of a compiler or a linker."""

    COMMAND: str

    SOURCE_EXTENSION: str
    TARGET_EXTENSION: str

    DEBUG_FLAGS: Flags
    RELEASE_FLAGS: Flags

    def preprocess(self, source: str) -> bytes:
        """Specify how the transformer preprocesses files.

        For example, the C preprocesser includes header files.

        Args:
            filename: The file path to process
        Returns:
            The contents of the preprocessed file
        """
        with open(source, "rb") as f:
            return f.read()

    @abstractmethod
    def transform(self, ctx: Context, source: str, target: str) -> None:
        """Performs the actual compiling/linking."""
        pass
