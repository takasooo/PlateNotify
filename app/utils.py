from app.database.database import SessionLocal, Session
from app.database.models import Plate, User, joinedload
import re

def normalize_plate(plate):
    plate = re.sub(r"[^A-Z0-9]", "", plate.upper())
    if re.match(r"^[A-Z]{3}\d{1,3}$", plate):  # Validate format (3 letters + 1-3 digits)
        return plate
    return None  # Return None if invalid

def register_plate(user_telegram_id: int, plate_number: str):
    session = SessionLocal()

    user = session.query(User).filter_by(telegram_id=user_telegram_id).first()
    if not user:
        user = User(telegram_id=user_telegram_id)
        session.add(user)
        session.commit()
        session.refresh(user)

    existing_plate = session.query(Plate).filter_by(plate_number=plate_number).first()
    if existing_plate:
        session.close()
        return False  # Plate already registered

    plate = Plate(owner_id=user.id, plate_number=plate_number)
    session.add(plate)
    session.commit()
    session.close()
    return True

def get_user_by_plate(plate_number):
    with SessionLocal() as session:
        plate = session.query(Plate).join(User).filter(Plate.plate_number == plate_number).first()
        return plate.owner.telegram_id if plate else None

