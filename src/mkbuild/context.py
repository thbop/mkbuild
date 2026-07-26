import sys
from dataclasses import dataclass
from pathlib import Path

from mkbuild.hash_handler import HashHandler


@dataclass
class Context:
    """Context object to keep track of paths and state."""

    def __post_init__(self) -> None:  # noqa: D105
        Path(self.BIN_PATH).mkdir(parents=True, exist_ok=True)

        self._hash_handler: HashHandler = HashHandler(self.BIN_PATH)

    SRC_PATH: str = "src"
    BIN_PATH: str = "bin"

    @property
    def IS_RELEASE(self) -> bool:
        """Checks if the user specified to build for release."""
        if len(sys.argv) > 1:
            return sys.argv[1] == "release"
        return False

    @property
    def HASH_HANDLER(self) -> HashHandler:
        """Returns the context hashhandler."""
        return self._hash_handler
