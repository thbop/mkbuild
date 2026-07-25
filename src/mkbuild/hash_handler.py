import hashlib
import json
from pathlib import Path

from mkbuild.compiler import Compiler
from mkbuild.context import Context

HASH_FILE_NAME = ".mkhashes"


class HashHandler:
    """Stores and keeps track of file hashes."""

    def __init__(self, ctx: Context):
        self.ctx = ctx
        self._load_hashes()

        self._mkhashes_path = Path(self.ctx.BIN_PATH, HASH_FILE_NAME)

    def _load_hashes(self) -> None:
        """Loads the hashes file."""
        try:
            with open(self._mkhashes_path) as f:
                self.hashes = json.load(f)
        except FileNotFoundError:
            self.hashes = {}

    def _dump_hashes(self):
        """Dumps the hashes to the hashes file."""
        with open(self._mkhashes_path, "w") as f:
            json.dump(self.hashes, f)

    def _hashfile(self, filename: str, compiler: Compiler) -> str:
        """Gets the sha256 hash of a preprocessed file."""
        data = compiler.preprocess(filename).encode()
        return hashlib.sha256(data).hexdigest()

    # @property
    # def _changed_sources(self):
    #     new_hashes = {src: self._hashfile(src) for src in sources}
    #     changed_sources = []
    #     for src, value in new_hashes.items():
    #         if hashes.get(src) and value == hashes[src]:
    #             continue
    #         changed_sources.append(src)
