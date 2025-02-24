from aiogram import Router, types
from aiogram.filters import Command
from app.utils import register_plate, get_user_by_plate, normalize_plate, re
from aiogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup

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

    raw_plate_number = parts[1]
    plate_number = normalize_plate(raw_plate_number)
    if register_plate(message.from_user.id, plate_number):
        await message.answer(f"Plate {plate_number} registered!")
    else:
        await message.answer("This plate is already registered.")

@router.message()
async def check_plate_mentions(message: types.Message):
    words = message.text.upper().split()
    for word in words:
        user_id = get_user_by_plate(word)
#if user_id and user_id != message.from_user.id:
        try:
            await message.bot.send_message(
                user_id,
                f"🚗 Your plate **{word}** was mentioned in **{message.chat.title}**.\n"
                f"[Jump to message](https://t.me/{message.chat.username}/{message.message_id})",
                parse_mode="Markdown",
                disable_web_page_preview=True
            )
        except Exception as e:
            print(f"Error sending DM: {e}")  # Log errors if user hasn't started the bot


