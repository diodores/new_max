# src/exceptions.py

class AppError(Exception):
    """
    Базовая ошибка приложения.
    """
    pass


# Webhook
class WebhookValidationError(AppError):
    """Ошибка валидации входящего webhook"""
    pass


class WebhookParseError(AppError):
    """Ошибка нормализации webhook"""
    pass


# Routing
class RouteNotFoundError(AppError):
    """
    Маршрут не найден.
    Это НЕ ошибка системы — это нормальный сценарий.
    """
    pass


class RoutingConfigError(AppError):
    """Ошибка конфигурации routing.json"""
    pass



# Rabbit
class RabbitConnectionError(AppError):
    """Не удалось подключиться к RabbitMQ"""
    pass


class RabbitChannelError(AppError):
    """Ошибка создания канала"""
    pass


class ExchangeNotInitializedError(AppError):
    """Exchange не инициализирован"""
    pass

class ProducerNotReadyError(AppError):
    """Producer не инициализирован"""
    pass


class PublishError(AppError):
    """Ошибка отправки в RabbitMQ"""
    pass