from datetime import datetime
import aiosqlite

DATABASE_PATH = "database.db"

async def init_db():
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                tg_id INTEGER PRIMARY KEY,
                wallet_address TEXT NOT NULL,
                private_key TEXT NOT NULL,
                created_at TEXT NOT NULL,
            )
        """)
        await db.commit()
async def get_user(tg_id: int):
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
                "SELECT wallet_address, private_key FROM users WHERE tg_id = ?",
                (tg_id,)
            )
        row = await cursor.fetchone()
        return row
async def add_user(tg_id: int, wallet_address: str, private_key: str):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
        "INSERT INTO users (tg_id, wallet_address, private_key, created_at) VALUES (?, ?, ?, ?)",
        (tg_id, wallet_address, private_key, created_at)
        )
        await db.commit()