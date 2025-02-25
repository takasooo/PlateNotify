from aiogram import Router, types
from aiogram.filters import Command
from app.utils import register_plate, get_user_by_plate, normalize_plate
from aiogram.types import Message
from aiogram.enums import ChatType
from app.database.models import Alert
from app.database.database import SessionLocal
from datetime import datetime
from app.database.models import Plate


router = Router()

@router.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("Welcome! Use /register <plate_number> to register your plate.")

@router.message(Command("register"))
async def register_cmd(message: Message):
    if message.chat.type != ChatType.PRIVATE:
        await message.reply("Please use this command in a private chat with me to register your plate. Go to @platenotifybot and press Start.")
        return

    parts = message.text.split(maxsplit=1)
    if len(parts) < 2:
        await message.answer("Usage: /register ABC123")
        return

    raw_plate_number = parts[1]
    plate_number = normalize_plate(raw_plate_number)

    if not plate_number:
        await message.answer("Invalid plate format! Use format: ABC1, XYZ12, DEF123.")
        return

    if register_plate(message.from_user.id, plate_number):
        await message.answer(f"Plate {plate_number} registered!")
    else:
        await message.answer("This plate is already registered.")

@router.message()
async def check_plate_mentions(message: types.Message):
    words = message.text.upper().split()
    checked_plates = set()

    for i in range(len(words)):
        for j in range(i+1, min(i+4, len(words)+1)):
            plate_candidate = ''.join(words[i:j])
            plate_candidate = normalize_plate(plate_candidate)
            if plate_candidate in checked_plates:
                continue
            
            checked_plates.add(plate_candidate)
            user_id = get_user_by_plate(plate_candidate)

            if user_id:
                try:
                    await message.bot.send_message(
                        user_id,
                        f"🚗 Your plate **{plate_candidate}** was mentioned in **{message.chat.title}**.\n"
                        f"[Jump to message](https://t.me/{message.chat.username}/{message.message_id})",
                        parse_mode="Markdown",
                        disable_web_page_preview=True
                    )

                    with SessionLocal() as session:
                        alert = Alert(
                            plate_id=session.query(Plate).filter_by(plate_number=plate_candidate).first().id,
                            mentioned_by=message.from_user.id,
                            chat_id=message.chat.id,
                            mentioned_at=datetime.now()
                        )
                        session.add(alert)
                        session.commit()

                except Exception as e:
                    print(f"Failed to send message to user {user_id}: {e}")