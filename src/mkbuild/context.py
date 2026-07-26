import sys
from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    """Context object to keep track of paths and state."""

    SRC_PATH: str = "src"
    BIN_PATH: str = "bin"

    @property
    def IS_RELEASE(self) -> bool:
        """Checks if the user specified to build for release."""
        if len(sys.argv) > 1:
            return sys.argv[1] == "release"
        return False
