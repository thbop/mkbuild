from abc import ABC, abstractmethod

from mkbuild.flags import Flags


class Compiler(ABC):
    """Abstract class that describes the properties of a compiler."""

    @property
    @abstractmethod
    def source_extension(self) -> str:
        """The source extension.

        For example: ".c"
        """
        pass

    @property
    @abstractmethod
    def target_extension(self) -> str:
        """The target extension.

        For example: ".o"
        """
        pass

    @property
    @abstractmethod
    def command(self) -> str:
        """The command to compile.

        Example:
        ```
        @property
        def command(self) -> str:
            return "gcc"
        ```

        """
        pass

    @property
    @abstractmethod
    def flags(self) -> Flags:
        """The default flags provided for compiling."""
        pass

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
