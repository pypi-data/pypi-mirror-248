from typing import AsyncGenerator

from aiobaseclient import BaseClient
from aiobaseclient.exceptions import ExternalServiceError


class TridentClient(BaseClient):
    async def response_processor(self, response):
        if response.status == 404:
            return None
        elif response.status != 200:
            data = await response.read()
            if hasattr(response, "request"):
                raise ExternalServiceError(response.request.url, response.status, data)
            else:
                raise ExternalServiceError(None, response.status, data)
        return response

    async def store(self, key: str, data: bytes, dry_run: bool = False) -> dict:
        url = f"/kv/{key}"
        response = await self.put(url, data=data, dry_run=dry_run)
        return await response.json()

    async def delete_key(self, key: str) -> dict:
        url = f"/kv/{key}"
        response = await self.delete(url)
        return await response.json()

    async def read(self, key: str) -> bytes:
        url = f"/kv/{key}"
        response = await self.get(url)
        return await response.read()

    async def read_chunks(self, key: str) -> AsyncGenerator[bytes, None]:
        url = f"/kv/{key}"
        response = await self.get(url)
        async for data, _ in response.content.iter_chunks():
            yield data

    async def exists(self, key: str) -> bool:
        url = f"/kv/{key}/exists"
        response = await self.get(url)
        if response is None:
            return False
        response = await response.json()
        return response["exists"]
