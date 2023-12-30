import dataclasses
from contextlib import asynccontextmanager

from fastapi import FastAPI
from izihawa_loglib import configure_logging
from starlette.requests import Request

from .configs import config
from .iroh_node import TridentIrohNode
from .storage import Storage


@dataclasses.dataclass
class State:
    storage: Storage
    iroh_node: TridentIrohNode


class TridentFastAPI(FastAPI):
    state: State


class TridentFastAPIRequest(Request):
    app: TridentFastAPI


@asynccontextmanager
async def lifespan(app: TridentFastAPI):
    configure_logging(config.get(dict))
    app.state = State(
        storage=Storage(config),
        iroh_node=TridentIrohNode(config)
    )
    yield
