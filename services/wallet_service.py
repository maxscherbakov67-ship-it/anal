from eth_account import Account
from database.db import add_user, get_user
import logging

logger = logging.getLogger(__name__)


async def get_or_create_wallet(tg_id: int) -> dict:
    user = await get_user(tg_id)

    if user is not None:
        wallet_address, private_key = user
        logger.info("Пользовать %s уже имеет кошелёк %s", tg_id, wallet_address)
        return {
            "wallet_address": wallet_address,
            "private_key": private_key,
            "is_new": False,
        }

    account = Account.create()
    wallet_address = account.address
    private_key = account.key.hex()

    await add_user(tg_id, wallet_address, private_key)
    logger.info("Создан новый кошелек для пользователя %s: %s", tg_id, wallet_address)

    return {
        "wallet_address": wallet_address,
        "private_key": private_key,
        "is_new": True,    
    }

    