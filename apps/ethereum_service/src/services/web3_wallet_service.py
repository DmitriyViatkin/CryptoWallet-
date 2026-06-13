from eth_account import Account

class Web3WalletService:

    async def import_wallet(self, private_key: str) -> str:
        """
        Импорт кошелька по приватному ключу.
        - Деривация адреса через eth_account
        - Валидация приватного ключа
        """
        try:
            account = Account.from_key(private_key)
            return account.address
        except Exception as e:
            raise ValueError(f"Invalid private key: {e}")