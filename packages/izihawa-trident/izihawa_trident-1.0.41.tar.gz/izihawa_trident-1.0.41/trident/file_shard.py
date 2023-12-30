import asyncio
import glob
import os
import time
import urllib.parse
from dataclasses import dataclass, field
from pathlib import Path

import aiofiles.os
from rbloom import Bloom

from .key_cache import KeyCache


@dataclass
class IntegrityReport:
    old_temporary_files: list[str] = field(default_factory=list)
    empty_files: list[str] = field(default_factory=list)
    ready: bool = False


class FileShard:
    def __init__(self, name: str, path: Path):
        self._name = name
        self._path = path
        self._key_cache = Bloom(10_000_000, 0.01)
        self._deletion_set = set()
        self._last_integrity_report = IntegrityReport()
        asyncio.get_event_loop().run_in_executor(None, self._check_integrity)

    @property
    def name(self) -> str:
        return self._name

    @property
    def path(self) -> Path:
        return self._path

    async def read(self, key: str) -> bytes:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if key in self._key_cache or os.path.exists(file_path):
            self._key_cache.add(key)
            if key in self._deletion_set:
                self._deletion_set.remove(key)
            async with aiofiles.open(file_path, "rb") as f:
                return await f.read()

    async def exists(self, key: str) -> bool:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        if (key in self._key_cache and key not in self._deletion_set) or os.path.exists(file_path):
            self._key_cache.add(key)
            return True
        return False

    async def write(self, key: str, value: bytes):
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        tmp_file_path = os.path.join(self.path, '~' + urllib.parse.quote(key))
        async with aiofiles.open(tmp_file_path, "wb") as f:
            await f.write(value)
            await f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_file_path, file_path)
        self._key_cache.add(key)
        if key in self._deletion_set:
            self._deletion_set.remove(key)

    async def delete(self, key: str) -> bool:
        file_path = os.path.join(self.path, urllib.parse.quote(key))
        try:
            await aiofiles.os.remove(file_path)
            self._deletion_set.add(key)
            return True
        except FileNotFoundError:
            return False

    def _check_integrity(self) -> IntegrityReport:
        current_time = time.time()
        for infile in glob.iglob(os.path.join(self._path, '*.*')):
            key = os.path.basename(infile)
            m_time = os.path.getmtime(infile)
            if m_time < current_time - 3600 * 4:
                if key.startswith('~') or key.endswith('~'):
                    self._last_integrity_report.old_temporary_files.append(infile)
                    continue
                if os.path.getsize(infile) == 0:
                    self._last_integrity_report.empty_files.append(infile)
                    continue
            self._key_cache.add(key)
        self._last_integrity_report.ready = True
        return self._last_integrity_report

    def get_integrity_report(self) -> IntegrityReport:
        return self._last_integrity_report
