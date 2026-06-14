class InfrastructureError(Exception):
    """Ошибки внутри слоя infrastructure"""


class CatalogRequestError(InfrastructureError):
    pass


class ItemNotFound(InfrastructureError):
    pass
