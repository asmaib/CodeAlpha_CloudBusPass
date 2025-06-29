from fastapi import FastAPI, Depends, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import SessionLocal, engine, Base
import os

# إنشاء الجداول
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Cloud Bus Pass System")

# ربط ملفات frontend
app.mount("/static", StaticFiles(directory="app/frontend"), name="static")

@app.get("/", response_class=FileResponse)
def serve_frontend():
    return FileResponse(os.path.join("app", "frontend", "index.html"))

# Dependency: get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ==== Bus Endpoints ====

@app.post("/buses/", response_model=schemas.Bus)
def create_bus(bus: schemas.BusCreate, db: Session = Depends(get_db)):
    return crud.create_bus(db, bus)

@app.get("/buses/", response_model=list[schemas.Bus])
def read_buses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_buses(db, skip=skip, limit=limit)

# ==== Booking Endpoints ====

@app.post("/bookings/", response_model=schemas.Booking)
def create_booking(booking: schemas.BookingCreate, db: Session = Depends(get_db)):
    bus = crud.get_bus(db, booking.bus_id)
    if not bus:
        raise HTTPException(status_code=404, detail="Bus not found")

    existing = db.query(models.Booking).filter(
        models.Booking.bus_id == booking.bus_id,
        models.Booking.seat_number == booking.seat_number
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="Seat already booked")

    return crud.create_booking(db, booking)

@app.get("/bookings/", response_model=list[schemas.Booking])
def read_bookings(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_bookings(db, skip=skip, limit=limit)
