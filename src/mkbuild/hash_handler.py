import hashlib
import json
from pathlib import Path

from mkbuild.compiler import Compiler
from mkbuild.context import Context
from mkbuild.exceptions import MKInvalidHashHandler
from mkbuild.sources import Sources

HASH_FILE_NAME = ".mkhashes"


class HashHandler:
    """Stores and keeps track of file hashes."""

    def __init__(self, ctx: Context):
        self.ctx = ctx

        self._mkhashes_path = Path(self.ctx.BIN_PATH, HASH_FILE_NAME)

    def __enter__(self):
        """Loads the hashes file."""
        self._load_hashes()

    def __exit__(self):
        """Dumps the hashes to the hashes file."""
        self._dump_hashes()

    def _load_hashes(self) -> None:
        """Loads the hashes file."""
        try:
            with open(self._mkhashes_path) as f:
                self._hashes = json.load(f)
        except FileNotFoundError:
            self._hashes = {}

    def _dump_hashes(self):
        """Dumps the hashes to the hashes file."""
        with open(self._mkhashes_path, "w") as f:
            json.dump(self._hashes, f)

    def _hashfile(self, filename: str, compiler: Compiler) -> str:
        """Gets the sha256 hash of a preprocessed file."""
        data = compiler.preprocess(filename).encode()
        return hashlib.sha256(data).hexdigest()

    def clear(self) -> None:
        """Clears all hashes--refreshing the cache."""
        if self._hashes is None:
            raise MKInvalidHashHandler()

        self._hashes = {}

    def get_changed_sources(self, sources: Sources) -> Sources:
        """Gets the sources that changed since last make."""
        if self._hashes is None:
            raise MKInvalidHashHandler()
        new_hashes = {
            src: self._hashfile(src, sources.collector) for src in sources
        }
        self._hashes |= new_hashes

        changed_sources = []
        for src, value in new_hashes.items():
            if self._hashes.get(src) and value == self._hashes[src]:
                continue
            changed_sources.append(src)

        return sources.copywith(changed_sources)
