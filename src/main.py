import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager
from src.rabbit.container import container
from src.api.webhook import router as webhook_router


consumer_tasks = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    await container.init()

    # стартуем consumers как фоновые задачи
    consumer_tasks.append(asyncio.create_task(container.whatsapp.start()))
    consumer_tasks.append(asyncio.create_task(container.max.start()))

    try:
        yield
    finally:
        for task in consumer_tasks:
            task.cancel()

        await container.shutdown()


app = FastAPI(lifespan=lifespan)
app.include_router(webhook_router, prefix="/webhook")



