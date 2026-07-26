import hashlib
import json
from pathlib import Path
from types import TracebackType
from typing import Self

from mkbuild.exceptions import MKInvalidHashHandler
from mkbuild.sources import Sources
from mkbuild.transformer import Transformer

HASH_FILE_NAME = ".mkhashes"


class HashHandler:
    """Stores and keeps track of file hashes."""

    def __init__(self, bin_path: str) -> None:

        self._mkhashes_path = Path(bin_path, HASH_FILE_NAME)
        self._hashes: dict[str, str] | None = None

    def __enter__(self) -> Self:
        """Loads the hashes file."""
        self._load_hashes()
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> bool | None:
        """Dumps the hashes to the hashes file."""
        self._dump_hashes()
        return None

    def _load_hashes(self) -> None:
        """Loads the hashes file."""
        try:
            with open(self._mkhashes_path) as f:
                self._hashes = json.load(f)
        except FileNotFoundError:
            self._hashes = {}

    def _dump_hashes(self) -> None:
        """Dumps the hashes to the hashes file."""
        with open(self._mkhashes_path, "w") as f:
            json.dump(self._hashes, f)

    def _hashfile(self, filename: str, transformer: Transformer) -> str:
        """Gets the sha256 hash of a preprocessed file."""
        data = transformer.preprocess(filename)
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

        # new_hashes = {
        #     src: self._hashfile(src, sources.transformer)
        #     for src in sources.sources
        # }

        # changed_sources = []
        # for src, new_hash in new_hashes.items():
        #     old_hash = self._hashes.get(src)
        #     if old_hash != new_hash:
        #         changed_sources.append(src)
        #         self._hashes[src] = new_hash

        changed_sources = []

        for src in sources.sources:
            # Resolve path to ensure absolute consistency
            src_key = str(Path(src).resolve())
            new_hash = self._hashfile(src, sources.transformer)
            old_hash = self._hashes.get(src_key)

            if old_hash != new_hash:
                changed_sources.append(src)
                self._hashes[src_key] = new_hash

        return sources.copywith(changed_sources)
