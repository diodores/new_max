#/home/deb/my_project/maxbot_rebbit/src/main.py
import asyncio
from fastapi import FastAPI
from contextlib import asynccontextmanager

from src.rabbit.container import container
from src.api.webhook import router as webhook_router
from src.api.exceptions.handler import register_exception_handlers

from src.logging_app import log_state, logger


consumer_tasks = []


@asynccontextmanager
async def lifespan(app: FastAPI):
    log_state("APP_STARTING")
    try:
        await container.init()
        log_state("CONTAINER_INITIALIZED")
    except Exception as e:
        logger.exception("container_init_failed error=%s", e)
        raise

    try:
        consumer_tasks.append(asyncio.create_task(container.whatsapp.start()))
        consumer_tasks.append(asyncio.create_task(container.max.start()))

        log_state("CONSUMERS_STARTED", count=len(consumer_tasks))

    except Exception as e:
        logger.exception("consumer_start_failed error=%s", e)
        raise

    try:
        yield

    finally:
        log_state("APP_SHUTTING_DOWN")

        for task in consumer_tasks:
            task.cancel()

        try:
            await container.shutdown()
            log_state("CONTAINER_STOPPED")
        except Exception as e:
            logger.exception("shutdown_failed error=%s", e)


app = FastAPI(lifespan=lifespan)

register_exception_handlers(app)
app.include_router(webhook_router, prefix="/webhook")

