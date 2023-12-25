import asyncio
import logging
import os
import sys
import urllib.parse
import zipfile

import aiofiles
import fire
from aiosumma import SummaClient

from trident.client import TridentClient


def process_zip(archive):
    zip_infos = archive.infolist()
    # iterate through each file
    for zip_info in zip_infos:
        prefix, suffix = zip_info.filename.lower().split("/", 1)
        suffix = urllib.parse.unquote(suffix)
        doi = prefix + "/" + suffix
        yield [doi.removesuffix(".pdf"), zip_info]


async def local_import(summa_client, trident_client, path: str, force: bool = False):
    logging.getLogger("statbox").info({"action": "import", "path": path})
    with zipfile.ZipFile(path) as archive:
        for doi, zip_info in process_zip(archive):
            document = await summa_client.get_one_by_field_value(
                "nexus_science",
                "id.dois",
                doi,
            )
            if not document:
                logging.getLogger("statbox").info(
                    {
                        "action": "not_found",
                        "doi": doi,
                    }
                )
                continue
            key = f'{document["id"]["nexus_id"]}.pdf'
            written = False
            if force or not await trident_client.exists(key):
                data = await asyncio.get_event_loop().run_in_executor(None, archive.read, zip_info)
                response = await trident_client.store(key, data, dry_run=True)
                file_shards = response['file_shards']
                for file_shard in file_shards:
                    file_path = os.path.join(file_shard, urllib.parse.quote(key))
                    tmp_file_path = os.path.join(file_shard, '~' + urllib.parse.quote(key))
                    async with aiofiles.open(tmp_file_path, "wb") as f:
                        await f.write(data)
                        await f.flush()
                        os.fsync(f.fileno())
                    os.replace(tmp_file_path, file_path)
                written = True
            logging.getLogger("statbox").info(
                {
                    "action": "stored",
                    "path": path,
                    "doi": doi,
                    "key": key,
                    "written": written,
                }
            )


async def import_file(summa_endpoint, trident_base_url, local_path):
    async with (
        SummaClient(endpoint=summa_endpoint) as summa_client,
        TridentClient(base_url=trident_base_url) as trident_client,
    ):
        await local_import(summa_client, trident_client, local_path)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    fire.Fire(import_file)
