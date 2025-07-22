import asyncio
import os
import logging
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from middlewares.db import DataBaseSession

from handlers.start import start
from handlers.gemini_handler import gemini
from handlers.payment import pay
from database.database import create_db, session_maker

load_dotenv()

async def main():
    dp = Dispatcher()
    await create_db()
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    bot = Bot(token=os.getenv('TOKEN_BOT'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp.include_routers(start, pay, gemini)
    await dp.start_polling(bot)



if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    print('Бот включен!')
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
