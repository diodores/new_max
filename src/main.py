from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.rabbit.container import Container
from  src.api.webhook import router as webhook_router


container = Container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await container.init()
    yield
    await container.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router, prefix="/webhook")



