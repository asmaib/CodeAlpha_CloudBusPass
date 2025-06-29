from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from uuid import uuid4
from fastapi import HTTPException
from . import models, schemas

# ==== Bus Functions ====

def create_bus(db: Session, bus: schemas.BusCreate):
    db_bus = models.Bus(**bus.dict())
    db.add(db_bus)
    try:
        db.commit()
        db.refresh(db_bus)
        return db_bus
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Bus with this number already exists.")


def get_buses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Bus).offset(skip).limit(limit).all()


def get_bus(db: Session, bus_id: int):
    return db.query(models.Bus).filter(models.Bus.id == bus_id).first()


# ==== Booking Functions ====

def create_booking(db: Session, booking: schemas.BookingCreate):
    ticket_code = str(uuid4())[:8]  # Generate short unique ticket code
    db_booking = models.Booking(
        passenger_name=booking.passenger_name,
        seat_number=booking.seat_number,
        bus_id=booking.bus_id,
        ticket_code=ticket_code,
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_bookings(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Booking).offset(skip).limit(limit).all()
