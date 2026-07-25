from dataclasses import dataclass


@dataclass(frozen=True)
class Context:
    """Context object to keep track of paths and state."""

    SRC_PATH: str = "src"
    BIN_PATH: str = "bin"
