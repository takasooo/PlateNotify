from database import SessionLocal
from models import Plate

def register_plate(user_id: int, plate_number: str):
    session = SessionLocal()
    existing_plate = session.query(Plate).filter_by(plate_number=plate_number).first()
    if existing_plate:
        session.close()
        return False  # Plate already registered

    plate = Plate(user_id=user_id, plate_number=plate_number)
    session.add(plate)
    session.commit()
    session.close()
    return True

def get_user_by_plate(plate_number: str):
    session = SessionLocal()
    plate = session.query(Plate).filter_by(plate_number=plate_number).first()
    session.close()
    return plate.user_id if plate else None
