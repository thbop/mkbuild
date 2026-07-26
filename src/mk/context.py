import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Context:
    """Context object to keep track of paths and state."""

    def __post_init__(self) -> None:  # noqa: D105
        Path(self.BIN_PATH).mkdir(parents=True, exist_ok=True)

    SRC_PATH: str = "src"
    BIN_PATH: str = "bin"

    @property
    def IS_RELEASE(self) -> bool:
        """Checks if the user specified to build for release."""
        if len(sys.argv) > 1:
            return sys.argv[1] == "release"
        return False
