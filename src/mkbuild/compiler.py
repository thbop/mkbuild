from dataclasses import dataclass

from mkbuild.flags import Flags


@dataclass
class Compiler:
    """A dataclass that describes the properties of a compiler."""

    COMMAND: str

    SOURCE_EXTENSION: str
    TARGET_EXTENSION: str

    DEBUG_FLAGS: Flags
    RELEASE_FLAGS: Flags

    def preprocess(self, filename: str) -> str:
        """Specify how the compiler preprocesses files.

        For example, the C preprocesser includes header files.

        Args:
            filename: The file path to process
        Returns:
            The contents of the preprocessed file
        """
        with open(filename) as f:
            return f.read()
