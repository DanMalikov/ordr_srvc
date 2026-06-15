class ApplicationError(Exception):
    """Ошибки внутри слоя application"""


class OrderNotFound(ApplicationError):
    pass
