import dataclasses
import mimetypes
import urllib.parse

from fastapi import APIRouter, Depends, HTTPException
from starlette.requests import Request
from starlette.responses import JSONResponse, Response

from .lifespan import TridentFastAPIRequest

router = APIRouter()


async def parse_body(request: Request):
    data: bytes = await request.body()
    return data


@router.put("/kv/{key}")
async def store(
    request: TridentFastAPIRequest,
    key: str,
    value: bytes = Depends(parse_body),
    dry_run: bool = False,
):
    if len(value) == 0:
        return HTTPException(status_code=422)
    response = await request.app.state.storage.store(key, value, dry_run)
    return response


@router.post("/broadcast/{key}/")
async def broadcast(
    request: TridentFastAPIRequest,
    key: str,
    doc_name: str,
    doc_key: str,
):
    path = await request.app.state.storage.exists(key)
    if path:
        return await request.app.state.iroh_node.store(doc_name, urllib.parse.unquote_plus(doc_key), path)


@router.get("/kv/{key}")
async def read(
    request: TridentFastAPIRequest,
    key: str,
) -> Response:
    data = await request.app.state.storage.read(key)
    if data:
        return Response(
            content=data,
            media_type=mimetypes.guess_type(key)[0],
            headers={}
        )
    raise HTTPException(status_code=404, detail="not_found")


@router.delete("/kv/{key}")
async def delete(
    request: TridentFastAPIRequest,
    key: str,
    dry_run: bool = False,
):
    return await request.app.state.storage.delete(key, dry_run)


@router.get("/kv/{key}/exists")
async def exists(request: TridentFastAPIRequest, key: str) -> Response:
    file_shard_name = await request.app.state.storage.exists(key)
    if file_shard_name:
        return JSONResponse(content={"exists": True, "first_file_shard": str(file_shard_name)})
    return JSONResponse(content={"exists": False}, status_code=404)


@router.get("/integrity_report/")
async def get_integrity_report(request: TridentFastAPIRequest) -> Response:
    integrity_reports = await request.app.state.storage.get_integrity_reports()
    return JSONResponse(content={
        file_share_name: dataclasses.asdict(integrity_report)
        for file_share_name, integrity_report in integrity_reports.items()
    })
