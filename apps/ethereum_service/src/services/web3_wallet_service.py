from eth_account import Account
import httpx
import os
from decimal import Decimal



from shared.messaging.schemas.wallet.wallet_operation_data import WalletOperation

ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = os.environ.get("ETHERSCAN_BASE_URL",
                                    "https://api.etherscan.io/api")
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


    async def get_transactions (self, address: str,
                                limit: int = 20) ->list[WalletOperation]:

        params = {
                  "chainid": 11155111,
                  "module":'account',
                  "action":'txlist',
                  "address":address,
                  "startblock": 0,
                  "endblock": 99999999,
                  "page": 1,
                  "offset": limit,
                  "sort": "desc",
                  "apikey": ETHERSCAN_API_KEY}
        async with httpx.AsyncClient() as client:
            response = await client.get(ETHERSCAN_BASE_URL, params=params)
            data= response.json()

        print(f"[ETHERSCAN RESPONSE] status={response.status_code} data={data}")

        if data.get("status") != "1":
            return []

        operations = []
        for tx in data.get("result", []):
            is_outgoing = tx["from"].lower() == address.lower()
            amount_eth = Decimal(tx["value"])/Decimal(10**18)

            operations.append(
                WalletOperation(
                    tx_hash=tx["hash"],
                    from_address=tx["from"],
                    to_address=tx["to"],
                    amount=amount_eth,
                    operation_type="withdrawal" if is_outgoing else "deposit",
                    status="failed" if tx.get("isError") == "1" else "completed",
                    block_number=int(tx["blockNumber"]),
                )

            )
        return operations