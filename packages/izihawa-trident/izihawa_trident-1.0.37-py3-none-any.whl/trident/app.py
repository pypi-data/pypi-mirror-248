from .lifespan import TridentFastAPI, lifespan
from .router import router

app = TridentFastAPI(lifespan=lifespan)
app.include_router(router)
