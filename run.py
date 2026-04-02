import asyncio
import logging
from aiogram import Bot,Dispatcher

from app.config import settings
from app.handlers.registration import register_router
from app.handlers.api import api_router
from app.handlers.client import client



async def main():
    bot = Bot(token=settings.TG_TOKEN)

    dp = Dispatcher()
    dp.include_routers(register_router, api_router, client)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info('Bot was stopped')

