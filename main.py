import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import commands, errors
from config import load_config
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime
from database.db import init_db

config = load_config()
async def main():
    storage = MemoryStorage()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=storage)
    await init_db()

    dp.include_router(commands.router)
    dp.include_router(errors.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                        format="%(name)s%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())
#penis