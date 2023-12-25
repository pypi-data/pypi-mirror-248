import dataclasses
from contextlib import asynccontextmanager

from fastapi import FastAPI
from izihawa_loglib import configure_logging
from starlette.requests import Request
from uhashring import HashRing

from .configs import config
from .file_shard import FileShard
from .storage import Storage


@dataclasses.dataclass
class State:
    storage: Storage


class TridentFastAPI(FastAPI):
    state: State


class TridentFastAPIRequest(Request):
    app: TridentFastAPI


@asynccontextmanager
async def lifespan(app: TridentFastAPI):
    configure_logging(config.get(dict))
    app.state = State(storage=Storage(config))
    yield
