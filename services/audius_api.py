import json
import logging
import os
import time

import aiohttp
from eth_account import Account
from eth_account.messages import encode_defunct

logger = logging.getLogger(__name__)

ENTRY_POINT = "https://api.audius.co"

class AudiusError(Exception):
    pass

def _sign_message(private_key: str, message: str) -> str:
    wallet = Account.from_key(private_key)
    signed = wallet.sign_message(encode_defunct(text=message))
    return signed.signature.hex()

async def get_creator_node(session: aiohttp.ClientSession) -> str:
    async with session.get(f"{ENTRY_POINT}/v1/nodes") as resp:
        body = await resp.text()
        if resp.status != 200:
            logger.error("Шлюз вернул %s: %s", resp.status, body)
            raise AudiusError("Не удалось получить список нод")
        data = json.loads(body)

    for node in data.get("data", []):
        if node.get("type") == "creator" and node.get("healthy"):
            return node["endpoint"]

    raise AudiusError("Не найдено ни одного здорового creator node")

async def _upload_file(
    session: aiohttp.ClientSession,
    creator_url: str,
    private_key: str,
    file_path: str,
    endpoint: str,
) -> str:
    wallet = Account.from_key(private_key)
    timestamp = int(time.time())
    message = f"{wallet.address}:{timestamp}"
    signature = _sign_message(private_key, message)

    headers = {
        "x-user-id": wallet.address,
        "x-signature": signature,
        "x-timestamp": str(timestamp),
    }

    with open (file_path, "rb") as f:
        form = aiohttp.FormData()
        form.add_field("file", f, filename=os.path.basename(file_path))

        url = f"{creator_url}/{endpoint}"
        async with session.post(url, data=form, headers=headers) as resp:
            body = await resp.text()
        if resp.status != 200:
            logger.error(
                "Загрузка %s не удалась: статус %s, тело: %s",
                file_path, resp.status, body,
            )
            raise AudiusError(f"Сервер отклонил файл: {resp.status}")

        result = json.loads(body)
    return result["data"][0]["id"]

async def upload_track(
    private_key: str,
    audio_path: str,
    title: str,
    genre: str,
    description: str = "",
    tags: str = "",
    cover_path: str | None = None,
    is_unlisted: bool = False,
) -> str:
    wallet = Account.from_key(private_key)

    async with aiohttp.ClientSession() as session:
        creator_url = await get_creator_node(session)
        logger.info("Выбран creator node: %s", creator_url)

        track_cid = await _upload_file(session, creator_url, private_key, audio_path, "tracks")
        logger.info("Аудио загружено, CID: %s", track_cid)

        cover_cid = None
        if cover_path and os.path.exists(cover_path):
            cover_cid = await _upload_file(session, creator_url, private_key, cover_path, "images")
            logger.info("Обложка загружена, CID: %s", cover_cid)

        metadata = {
            "title": title,
            "genre": genre,
            "description": description,
            "tags": tags,
            "track_cid": track_cid,
            "cover_art_cid": cover_cid,
            "is_unlisted": is_unlisted
        }

        metadata_str = json.dumps(metadata, sort_keys=True, separators=(",", ":"))
        signature = _sign_message(private_key, metadata_str)

        headers = {
            "x-user-id": wallet.address,
            "x-signature": signature,
            "x-signature-data": metadata_str
        }
        async with session.post(f"{creator_url}/tracks", json=metadata, headers=headers) as resp:
            body = await resp.text()
            if resp.status not in (200, 201):
                logger.error("Регистрация трека не удалась: %s, тело: %s", resp.status, body)
                raise AudiusError(f"Audius отклонил трек: {resp.status}")
            result = json.loads(body)

    track_id = result["data"][0]["id"]
    logger.info("Трек зарегистрирован: %s", track_id)
    return f"https://audius.co/{wallet.address}/{track_id}"