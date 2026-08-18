
import asyncio
import logging
import config
from aiogram import Bot, Dispatcher
from handlers.user import router as user_router
from services.xui_api import xui_client

logging.basicConfig(level=logging.INFO)

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(user_router)

    await xui_client.login()

    try:
        await dp.start_polling(bot)
    finally:
        await xui_client.close()
        await bot.session.close()

if __name__ == "__main__":
    asyncio.run(main())
