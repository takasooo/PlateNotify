import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from app.database.database import engine
from app.database.models import Base

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

async def main():
    load_dotenv()  # Load environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    Base.metadata.create_all(bind=engine)  # Initialize DB tables
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    logger.info("🤖 Bot started successfully!")

    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Bot encountered an error: {e}")

if __name__ == '__main__':
    try:
        print(os.getenv("DB_URL"))
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Goodbye!')