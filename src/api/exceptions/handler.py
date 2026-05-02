#src/api/exceptions/handlers.py
from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
from src.api.response import error, ignored

from src.exceptions import (
    AppError,

    WebhookValidationError,
    WebhookParseError,

    RouteNotFoundError,
    RoutingConfigError,

    RabbitConnectionError,
    RabbitChannelError,
    ExchangeNotInitializedError,

    ProducerNotReadyError,
    PublishError,
)


def register_exception_handlers(app: FastAPI):


    # Всё что не покрыл, всё неизвестное
    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        return JSONResponse(
            status_code=500,
            content=error("app_error", str(exc))
        )


    # WEBHOOK
    @app.exception_handler(WebhookValidationError)
    async def webhook_validation_handler(request: Request, exc: WebhookValidationError):
        return JSONResponse(
            status_code=400,
            content=error("webhook_validation_error")
        )

    @app.exception_handler(WebhookParseError)
    async def webhook_parse_handler(request: Request, exc: WebhookParseError):
        return JSONResponse(
            status_code=400,
            content=error("webhook_parse_error"),
        )


    # ROUTING
    # @app.exception_handler(RouteNotFoundError)
    # async def route_not_found_handler(request: Request, exc: RouteNotFoundError):
    #     # нормальный сценарий → не ошибка системы <-- ВАЖНО!!!
    #     return JSONResponse(
    #         status_code=200,
    #         content={
    #             "ignored": True,
    #         },
    #     )

    @app.exception_handler(RoutingConfigError)
    async def routing_config_handler(request: Request, exc: RoutingConfigError):
        return JSONResponse(
            status_code=500,
            content=error("routing_config_error", str(exc))
        )


    # RABBIT
    @app.exception_handler(RabbitConnectionError)
    async def rabbit_connection_handler(request: Request, exc: RabbitConnectionError):
        return JSONResponse(
            status_code=500,
            content=error("rabbit_connection_error"),
        )

    @app.exception_handler(RabbitChannelError)
    async def rabbit_channel_handler(request: Request, exc: RabbitChannelError):
        return JSONResponse(
            status_code=500,
            content=error("rabbit_channel_error"),
        )

    @app.exception_handler(ExchangeNotInitializedError)
    async def exchange_not_initialized_handler(request: Request, exc: ExchangeNotInitializedError):
        return JSONResponse(
            status_code=500,
            content=error("exchange_not_initialized"),
        )


    # PRODUCER
    @app.exception_handler(ProducerNotReadyError)
    async def producer_not_ready_handler(request: Request, exc: ProducerNotReadyError):
        return JSONResponse(
            status_code=500,
            content=error("producer_not_ready"),
        )

    @app.exception_handler(PublishError)
    async def publish_error_handler(request: Request, exc: PublishError):
        # 502 = upstream problem (Rabbit)
        return JSONResponse(
            status_code=502,
            content=error("publish_error"),
        )