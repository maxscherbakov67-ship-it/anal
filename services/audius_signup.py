import asyncio
import logging

import aiohttp
from web3 import Web3

from services.audius_api import AudiusError

logger = logging.getLogger(__name__)

USER_FACTORY_ADDRESS = "0x0000000000000000000000000000000000000000"  # ← подставить реальный
USER_FACTORY_ABI = [
    {
        "name": "registerUser",
        "type": "function",
        "inputs": [
            {"name": "_handle", "type": "bytes32"},
            {"name": "_wallet", "type": "address"},
        ],
        "outputs": [],
        "stateMutability": "nonpayable",
    }
]

RELAY_URL = "https://relay.audius.co" 


def make_handle(tg_id: int) -> str:
    return f"tg{tg_id}"[:32]

def _handle_to_bytes32(handle:str) -> bytes:
    return Web3.to_bytes(text=handle).ljust(32, b"\x00")

def _encode_register_calldata(handle:str, wallet_address: str) -> str:
    w3 = Web3()
    contract = w3.eth.contract(address=USER_FACTORY_ADDRESS, abi = USER_FACTORY_ABI)
    return contract.functions.registerUser(
        _handle_to_bytes32(handle), wallet_address
    ).encode_abi()

async def register_user_on_audius(private_key: str, tg_id: int) -> str:
    wallet = Web3().eth.account.from_key(private_key)
    handle = make_handle(tg_id)

    async with aiohttp.ClientSession() as session:
        calldata = _encode_register_calldata(handle, wallet_address)

        payload = {
            "contractAddress": USER_FACTORY_ADDRESS,
            "contractName": "UserFactory",
            "encodedData": calldata
        }
        async with session.post(f"{RELAY_URL}/relay", json=payload) as resp:
            body = await resp.text()
            if resp.status != 200:
                logger.error("Relay отказал: %s тело: %s", resp.status, body)
                raise AudiusError("Relay не принял транзакцию регистрации")
            tx_hash = (await resp.json()).get("txHash")

        logger.info("Транзакция регистрации отправлена: %s", tx_hash)

        for attempt in range(30):
            await asyncio.sleep(2)
            async with session.get(f"{RELAY_URL}/relay/tx_status", params={"txHash": tx_hash}) as resp:
                status = (await resp.json()).get("status")
            if status == "SUCCESS":
                logger.info("Пользователь %s зарегистрирован в Audius", handle)
                return handle
            if status == "FAILED":
                raise AudiusError("Транзакция регистрации не прошла")

            raise AudiusError("Не дождались подтверждения транзакции")