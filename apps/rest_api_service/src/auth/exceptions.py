class AuthError(Exception):
    """Базовое исключение для аутентификации"""
    pass

class UserAlreadyExistsError(AuthError):
    """Пользователь с таким username уже существует"""
    pass

class EmailAlreadyExistsError(AuthError):
    """Пользователь с таким email уже существует"""
    pass

class WeakPasswordError(AuthError):
    """Пароль не прошёл валидацию (слишком простой)"""
    pass