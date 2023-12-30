import asyncio
from pathlib import Path

import confuse
import iroh


class TridentIrohNode:
    def __init__(self, config: confuse.Configuration):
        self._iroh_node = iroh.IrohNode(config['iroh']['path'].get('str'))

        if 'author' not in config['iroh']:
            raise RuntimeError(f"Setup following `author` in `iroh.author` attribute of config.yaml")
        self._author = config['iroh']['author'].get(str)

        self._docs = {}
        for doc in config['iroh']['docs'].get(list):
            self._docs[doc['name']] = self._iroh_node.doc_open(iroh.NamespaceId.from_string(doc['id']))

    async def store(self, doc_name: str, key: str, path: Path):
        return await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: self._docs[doc_name].import_file,
            self._author,
            key.encode(),
            path,
            True,
            None
        )

    async def read(self, doc_name: str, key: str) -> bytes:
        query_options = iroh.QueryOptions(iroh.SortBy.KEY_AUTHOR, direction=iroh.SortDirection.ASC)
        entry = self._docs[doc_name].get_one(iroh.Query.key_exact(key.encode(), opts=query_options))
        if entry is not None:
            return await asyncio.get_running_loop().run_in_executor(
                None,
                entry.content_bytes,
                self._docs[doc_name]
            )

