import asyncio
from aiogram import Bot, Dispatcher
from bot.handlers import commands
from config import load_config
import logging
from aiogram.fsm.storage.memory import MemoryStorage
from datetime import datetime

config = load_config()
async def main():
    storage = MemoryStorage()
    bot = Bot(token=config.bot_token)
    dp = Dispatcher(storage=storage)

    dp.include_router(commands.router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename="log.log", filemode="a",
                        format="%(name)s%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main())