from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generic, TypeVar

from mkbuild.context import Context
from mkbuild.flags import Flags

SourceType = TypeVar("SourceType", str, list[str])
TargetType = TypeVar("TargetType", str, None)


@dataclass(frozen=True)
class Transformer(ABC, Generic[SourceType, TargetType]):
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
    def transform(
        self, ctx: Context, source: SourceType, target: TargetType
    ) -> None:
        """Performs the actual compiling/linking."""
        pass
