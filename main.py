import asyncio
from aiogram import Bot, Dispatcher
from config import BOT_TOKEN
from handlers import router
from database import engine
from models import Base

async def main():
    Base.metadata.create_all(bind=engine)  # Initialize DB tables
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
