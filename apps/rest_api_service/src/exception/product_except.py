class ProductError(Exception):
    """Базовое исключение для бизнес-логики продуктов"""
    pass

class ProductAlreadyExistsError(ProductError):
    """У этого пользователя уже есть продукт с таким названием"""
    pass

class InvalidWalletAddressError(ProductError):
    """Некорректный формат крипто-кошелька"""
    pass

class InvalidPriceError(ProductError):
    """Недопустимая цена (например, отрицательная или нулевая)"""
    pass

class ProductNotFoundError(ProductError):
    """Продукт не найден в базе данных"""
    pass

class ProductAccessDeniedError(ProductError):
    """У пользователя нет прав на редактирование этого продукта"""
    pass