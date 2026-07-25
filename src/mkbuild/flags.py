import platform
from abc import ABC, abstractmethod

from mkbuild.exceptions import MKUnsupportedOS


class Flags(ABC):
    """An abstract class to represent various flags compilers and linkers."""

    @abstractmethod
    @property
    def get(self) -> str:
        """Gets the default compiler/linker flags."""
        pass


class OSFlags(Flags):
    """An abstract flags class that is discriminates based off platform."""

    @abstractmethod
    @property
    def windows(self) -> str:
        """The default flags for windows."""
        pass

    @abstractmethod
    @property
    def linux(self) -> str:
        """The default flags for linux."""
        pass

    @property
    def get(self) -> str:
        """Gets the default compiler/linker flags."""
        target_os = platform.system()
        match target_os:
            case "Windows":
                return self.windows
            case "Linux":
                return self.linux
            case _:
                raise MKUnsupportedOS()
