from app.database.database import SessionLocal, Session
from app.database.models import Plate, User, joinedload
import re

def normalize_plate(plate):
    return re.sub(r"[^A-Z0-9]", "", plate.upper())

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
        plate = session.query(Plate).filter_by(plate_number=plate_number).first()
        if plate:
            session.add(plate)
            return plate.owner.telegram_id
        return None

