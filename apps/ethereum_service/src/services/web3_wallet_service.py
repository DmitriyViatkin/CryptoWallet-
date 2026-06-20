import logging
import asyncio
from eth_account import Account
import httpx
from web3 import Web3
from shared.crypto.encryption import encrypt_private_key, decrypt_private_key
import os
from decimal import Decimal
from shared.messaging.schemas.wallet.wallet_operation_data import WalletOperation

logger = logging.getLogger(__name__)

ETHERSCAN_API_KEY = os.environ.get("ETHERSCAN_API_KEY")
ETHERSCAN_BASE_URL = os.environ.get("ETHERSCAN_BASE_URL",
                              "https://api.etherscan.io/api")
RPC_URL = os.environ.get("RPC_URL", "https://eth.llamarpc.com")
w3 = Web3(Web3.HTTPProvider(RPC_URL))
CHAIN_ID = int(os.environ.get("CHAIN_ID", 11155111))



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

    async def create_wallet(self):
        """
        Генерация нового кошельк
        """

        account = w3.eth.account.create()
        address = account.address
        private_key = account.key.hex()
        return address, encrypt_private_key(private_key)


    async def get_transactions (self, address: str,
                                limit: int = 20) ->list[WalletOperation]:

        params = {
                  "chainid": CHAIN_ID,
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
            response.raise_for_status()
            data= response.json()

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


    async def send_transaction(self, address_from:str, encrypted_private_key: str,
                               address_to:str, amount):
        if not w3.is_connected():
            logger.critical("Ошибка подключения к Ethereum сети")
            return None
        logger.info(f"Initiating tx from {address_from} to {address_to}, amount: {amount} ETH")
        private_key = await asyncio.to_thread(decrypt_private_key, encrypted_private_key)
        try:
            nonce = await  asyncio.to_thread(w3.eth.get_transaction_count,address_from)
            fee_data = await asyncio.to_thread(w3.eth.fee_history,1,"latest", [50])
            base_fee = fee_data["baseFeePerGas"][-1]
            priority_fee=w3.to_wei('1','gwei')

            tx = {
                'nonce': nonce,
                'to': address_to,
                'value': w3.to_wei(amount, 'ether'),
                "gas": 21000,
                "maxFeePerGas": base_fee + priority_fee,      # ← динамічно
                "maxPriorityFeePerGas": priority_fee,
                "chainId": CHAIN_ID,
            }
            signed_tx = w3.eth.account.sign_transaction(tx, private_key)
            tx_hash = await asyncio.to_thread(w3.eth.send_raw_transaction, signed_tx.raw_transaction)
            tx_receipt = await asyncio.to_thread( w3.eth.wait_for_transaction_receipt, tx_hash)

            logger.info(
                f"Transaction mined successfully. Block: {tx_receipt.get('blockNumber')}")


            return tx_receipt
        except Exception as e:
            logger.exception(f"Transaction failed from {address_from} to {address_to}")
            return None