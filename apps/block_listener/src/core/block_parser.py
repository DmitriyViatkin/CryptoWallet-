import logging
from decimal import Decimal

from web3 import AsyncWeb3

logger = logging.getLogger(__name__)


async def parse_block_transactions(
    w3: AsyncWeb3,
    block_number: int,
    our_addresses: set[str],
) -> list[dict]:
    """
    Загружает блок, фильтрует транзакции по нашим адресам,
    возвращает список dict-ов для публикации события TxDetectedEvent.
    """
    try:
        block = await w3.eth.get_block(block_number, full_transactions=True)
    except Exception as e:
        logger.error(f"Failed to fetch block {block_number}: {e}")
        return []

    matched = []

    for tx in block["transactions"]:
        from_addr = tx["from"].lower()
        to_addr = (tx.get("to") or "").lower()

        if from_addr not in our_addresses and to_addr not in our_addresses:
            continue

        try:
            receipt = await w3.eth.get_transaction_receipt(tx["hash"])
            status = "completed" if receipt["status"] == 1 else "failed"
        except Exception as e:
            logger.warning(f"Failed to get receipt for {tx['hash'].hex()}: {e}")
            status = "unknown"

        matched.append({
            "tx_hash": tx["hash"].hex(),
            "from_address": tx["from"],
            "to_address": tx.get("to"),
            "amount": Decimal(tx["value"]) / Decimal(10 ** 18),
            "block_number": block_number,
            "status": status,
        })

        logger.info(f"Matched tx: {tx['hash'].hex()} | status: {status}")

    return matched