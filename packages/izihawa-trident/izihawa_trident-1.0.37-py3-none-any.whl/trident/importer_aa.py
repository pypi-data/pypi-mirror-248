import asyncio
import logging
import os
import sys

import aiofiles
import fire
import orjson
from aiokit import MultipleAsyncExecution
from aiosumma import SummaClient

from trident.client import TridentClient


async def job(summa_client: SummaClient, trident_client: TridentClient, zlibrary_id, path, extension, md5):
    if extension not in ['pdf', 'epub']:
        return
    document = await summa_client.get_one_by_field_value('nexus_science', 'id.zlibrary_ids', zlibrary_id)
    logging.getLogger("statbox").info({"action": "try_store", "path": path, "extension": extension, 'md5': md5})
    if not document:
        return

    key = f'{document["id"]["nexus_id"]}.{extension}'

    if 'links' not in document:
        if await trident_client.exists(key):
            return
        async with aiofiles.open(path, 'rb') as f:
            logging.getLogger("statbox").info({"action": "store", "key": key, "aa_path": path})
            await trident_client.store(key, await f.read())
        return

    for link in document['links']:
        if link.get('md5') == md5:
            if await trident_client.exists(key):
                return
            async with aiofiles.open(path, 'rb') as f:
                logging.getLogger("statbox").info({"action": "stored", "key": key, "aa_path": path})
                await trident_client.store(key, await f.read())
            return


async def local_import(summa_client, trident_client, aa_dictionary, aa_meta: str, aa_path: str, force: bool = False):
    logging.getLogger("statbox").info({"action": "import", "aa_meta": aa_meta, "aa_path": aa_path})

    prepared_files = []
    for root, dirs, files in os.walk(aa_path):
        for filename in files:
            if filename.endswith('.torrent'):
                continue
            zlibrary_id = filename.split('__')[3]
            md5, extension = aa_dictionary.get(zlibrary_id)
            if not md5:
                continue
            prepared_files.append((zlibrary_id, root + '/' + filename, extension, md5))

    executor = MultipleAsyncExecution(4)

    for zlibrary_id, path, extension, md5 in prepared_files:
        await executor.execute(job(summa_client, trident_client, zlibrary_id, path, extension, md5))

    await asyncio.sleep(10)
    await executor.join()


async def import_file():
    summa_endpoint = 'localhost:10082'
    trident_base_url = 'http://localhost:7080'
    aa_meta = '/home/pasha/annas_archive_meta__aacid__zlib3_records__20230808T014342Z--20231102T230010Z.jsonl'
    aa_path = '/home/pasha/aa/20230808'
    aa_dictionary = {}
    with open(aa_meta) as f:
        for line in f:
            a_line = orjson.loads(line)
            if 'missing' in a_line['metadata']:
                continue
            aa_dictionary[str(a_line['metadata']['zlibrary_id'])] = (a_line['metadata']['md5_reported'], a_line['metadata']['extension'])

    async with (
        SummaClient(endpoint=summa_endpoint) as summa_client,
        TridentClient(base_url=trident_base_url) as trident_client,
    ):
        await local_import(summa_client, trident_client, aa_dictionary, aa_meta, aa_path)


def main():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    fire.Fire(import_file)


main()
