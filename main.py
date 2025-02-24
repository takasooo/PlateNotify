import os
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from app.handlers import router
from app.database.database import engine
from app.database.models import Base

async def main():
    load_dotenv()  # Load environment variables
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    Base.metadata.create_all(bind=engine)  # Initialize DB tables
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        print(os.getenv("DB_URL"))
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Goodbye!')