from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Generic, TypeVar

from mkbuild.flags import Flags

if TYPE_CHECKING:
    from mkbuild.context import Context

SourceType = TypeVar("SourceType", str, list[str])
TargetType = TypeVar("TargetType", str, None)


@dataclass(frozen=True, kw_only=True)
class Transformer(ABC, Generic[SourceType, TargetType]):
    """A dataclass that describes the properties of a compiler or a linker."""

    COMMAND: str

    SOURCE_EXTENSION: str
    TARGET_EXTENSION: str

    FLAGS: Flags | None
    DEBUG_FLAGS: Flags | None
    RELEASE_FLAGS: Flags | None

    def _merge_flags(self, is_release: bool) -> str:
        flags = self.FLAGS.get() + " " if self.FLAGS else ""
        flags += (
            (self.RELEASE_FLAGS.get() if self.RELEASE_FLAGS else "")
            if is_release
            else (self.DEBUG_FLAGS.get() if self.DEBUG_FLAGS else "")
        )
        return flags

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
