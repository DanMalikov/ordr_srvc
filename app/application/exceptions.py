class ApplicationError(Exception):
    """Ошибки внутри слоя application"""


class OrderNotFound(ApplicationError):
    pass


class ItemOutOfStock(ApplicationError):
    pass


class PaymentClientNotAvailable(ApplicationError):
    pass
