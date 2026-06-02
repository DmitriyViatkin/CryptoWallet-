from src.users.models.wallets import Wallet
from src.users.models.wallet_operations import WalletOperation
from src.users.repositories.wallet_repo import WalletRepository
from src.users.repositories.wallet_operation_repo import WalletOperationRepository
from src.users.services.base_service import BaseService


class WalletService(BaseService[Wallet]):
    def __init__(
        self,
        wallet_repo: WalletRepository,
        wallet_operation_repo: WalletOperationRepository,
    ) -> None:
        super().__init__(wallet_repo)
        self._wallet_repo = wallet_repo
        self._operation_repo = wallet_operation_repo

    # ── Wallet ────────────────────────────────────────────────────────────────

    async def create_wallet(self, user_id: int, title: str, wallet_type: str) -> Wallet:
        """
        Генерація нового гаманця.
        - web3.py: генерація приватного ключа + адреси
        - Шифрування приватного ключа (Fernet/AES)
        - Перевірка UniqueConstraint(user_id, wallet_address)
        - Збереження в БД
        """
        raise NotImplementedError

    async def import_wallet(
        self, user_id: int, title: str, private_key: str, wallet_type: str
    ) -> Wallet:
        """
        Імпорт гаманця по приватному ключу.
        - Деривація адреси через web3.py
        - Перевірка унікальності: get_by_address_and_user(address, user_id)
        - Шифрування приватного ключа перед збереженням
        """
        raise NotImplementedError

    async def get_user_wallets(self, user_id: int) -> list[Wallet]:
        return await self._wallet_repo.get_by_user_id(user_id)

    async def get_balance(self, wallet_address: str) -> dict:
        """
        Баланс з блокчейну через web3.py.
        Повертає {"address": ..., "balance_wei": ..., "balance_eth": ...}
        """
        raise NotImplementedError

    # ── WalletOperation ───────────────────────────────────────────────────────

    async def get_wallet_operations(self, wallet_id: int) -> list[WalletOperation]:
        """Всі операції конкретного гаманця."""
        return await self._operation_repo.get_by_wallet_id(wallet_id)

    async def get_operation_by_tx(self, tx_hash: str) -> WalletOperation | None:
        """Пошук операції по tx_hash (для дедуплікації)."""
        return await self._operation_repo.get_by_tx_hash(tx_hash)

    async def record_operation(
        self,
        wallet_id: int,
        tx_hash: str,
        from_address: str,
        to_address: str,
        amount: str,
        operation_type: str,
        block_number: int | None = None,
    ) -> WalletOperation:
        """
        Запис операції після on-chain транзакції.
        - Перевірка унікальності tx_hash (get_by_tx_hash) — дедуплікація
        - Статус = PENDING за замовчуванням (з моделі)
        - Використовується TaskIQ воркером після підтвердження блоку
        """
        existing = await self._operation_repo.get_by_tx_hash(tx_hash)
        if existing:
            return existing
        raise NotImplementedError

    async def update_operation_status(
        self, tx_hash: str, new_status: str
    ) -> WalletOperation | None:
        """
        Оновлення статусу операції (PENDING → CONFIRMED/FAILED).
        Викликається TaskIQ після перевірки блоку.
        """
        operation = await self._operation_repo.get_by_tx_hash(tx_hash)
        if not operation:
            return None
        return await self._operation_repo.update(operation, status=new_status)