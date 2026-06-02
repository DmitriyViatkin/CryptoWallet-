from src.users.models.users import User
from src.users.repositories.user_repo import UserRepository
from src.users.repositories.permission_repo import PermissionRepository
from src.users.services.base_service import BaseService


class UserService(BaseService[User]):
    def __init__(
        self,
        user_repo: UserRepository,
        permission_repo: PermissionRepository,
    ) -> None:
        super().__init__(user_repo)
        self._user_repo = user_repo
        self._permission_repo = permission_repo

    async def register(self, username: str, email: str, password: str) -> User:
        """
        Реєстрація нового юзера.
        - Перевірка унікальності email
        - Хешування пароля (passlib/bcrypt)
        - Створення User + Permission запису
        - Планування TaskIQ задачі на надання chat_access через 1 хв
        """
        raise NotImplementedError

    async def login(self, email: str, password: str) -> dict:
        """
        Логін юзера.
        - Перевірка email існує
        - Верифікація пароля
        - Генерація access + refresh JWT токенів
        - Повертає {"access_token": ..., "refresh_token": ...}
        """
        raise NotImplementedError

    async def refresh_token(self, refresh_token: str) -> dict:
        """
        Оновлення access токену по refresh токену.
        - Валідація refresh токену (перевірка підпису, expiry)
        - Генерація нового access токену
        """
        raise NotImplementedError

    async def get_profile(self, user_id: int) -> User | None:
        return await self._user_repo.get_by_id(user_id)

    async def update_profile(self, user_id: int, **kwargs) -> User | None:
        """
        Оновлення профілю.
        - Якщо передається новий email — перевірка унікальності
        - Якщо передається новий пароль — хешування
        """
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            return None
        raise NotImplementedError

    async def deactivate(self, user_id: int) -> User | None:
        """М'яке видалення — встановлює is_active=False."""
        user = await self._user_repo.get_by_id(user_id)
        if not user:
            return None
        return await self._user_repo.update(user, is_active=False)

    async def get_active_users(self) -> list[User]:
        return await self._user_repo.get_active_users()