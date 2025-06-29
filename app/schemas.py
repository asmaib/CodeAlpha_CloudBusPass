from pydantic import BaseModel
from datetime import datetime

# ==== Bus Schemas ====

class BusBase(BaseModel):
    bus_number: str
    origin: str
    destination: str
    departure_time: datetime
    total_seats: int
    price: float

class BusCreate(BusBase):
    pass

class Bus(BusBase):
    id: int

    class Config:
        orm_mode = True


# ==== Booking Schemas ====

class BookingBase(BaseModel):
    passenger_name: str
    seat_number: int

class BookingCreate(BookingBase):
    bus_id: int

class Booking(BookingBase):
    id: int
    booking_time: datetime
    ticket_code: str
    bus_id: int

    class Config:
        orm_mode = True
