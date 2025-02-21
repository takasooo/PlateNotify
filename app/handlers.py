from aiogram import Router, types
from aiogram.filters import Command
from utils import register_plate, get_user_by_plate
from aiogram.types import Message

router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Welcome! Use /register <plate_number> to register your plate.")

@router.message(Command("register"))
async def register_cmd(message: Message):
    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /register ABC123")
        return

    plate_number = parts[1].upper()
    if register_plate(message.from_user.id, plate_number):
        await message.answer(f"Plate {plate_number} registered!")
    else:
        await message.answer("This plate is already registered.")

@router.message()
async def check_plate_mentions(message: Message):
    words = message.text.upper().split()
    for word in words:
        user_id = get_user_by_plate(word)
        if user_id and user_id != message.from_user.id:
            await message.bot.send_message(user_id, f"Your plate {word} was mentioned in chat!")
