import platform
from dataclasses import dataclass

from mkbuild.exceptions import MKUnsupportedOS


@dataclass(frozen=True)
class Flags:
    """A dataclass to represent various flags for compilers and linkers."""

    FLAGS: str

    def get(self) -> str:
        """Gets the default compiler/linker flags."""
        return self.FLAGS or ""


@dataclass(frozen=True)
class OSFlags(Flags):
    """A dataclass that discriminates flags based off platform."""

    WINDOWS: str
    LINUX: str

    def get(self) -> str:
        """Gets the default compiler/linker flags."""
        target_os = platform.system()
        match target_os:
            case "Windows":
                return self.FLAGS + " " + self.WINDOWS
            case "Linux":
                return self.FLAGS + " " + self.LINUX
            case _:
                raise MKUnsupportedOS()
