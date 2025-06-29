from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from .database import Base

class Bus(Base):
    __tablename__ = "buses"

    id = Column(Integer, primary_key=True, index=True)
    bus_number = Column(String, unique=True, nullable=False)
    origin = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    departure_time = Column(DateTime, nullable=False)
    total_seats = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)

    bookings = relationship("Booking", back_populates="bus")


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    passenger_name = Column(String, nullable=False)
    seat_number = Column(Integer, nullable=False)
    booking_time = Column(DateTime, default=datetime.utcnow)
    ticket_code = Column(String, unique=True, nullable=False)

    bus_id = Column(Integer, ForeignKey("buses.id"))
    bus = relationship("Bus", back_populates="bookings")
