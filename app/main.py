from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from contextlib import asynccontextmanager
from .models import Payload
from .schemas import PayloadInput, PayloadOutput
from .database import Base, engine, init_db, SessionLocal
from .refactorer import get_or_create_payload
import logging

logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to create a new payload
@app.post("/payload", response_model=PayloadOutput)
async def create_payload(payload: PayloadInput, db: Session = Depends(get_db)):
    try:
        payload_id, interleaved_output = get_or_create_payload(db, payload)
        logging.info(f"Created payload with ID {payload_id}")
        return {"id": payload_id, "message": "Payload created"}
    except Exception as e:
        logging.error(f"Error creating payload: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
    
# Endpoint to read an existing payload by ID
async def read_payload(payload_id: str, db: Session = Depends(get_db)):
    try:
        payload = db.query(Payload).filter(Payload.id == payload_id).first()
        if not payload:
            logging.error(f"Payload with ID {payload_id} not found")
            raise HTTPException(status_code=404, detail="Payload not found")
        logging.info(f"Retrieved payload with ID {payload_id}")
        return {"id": str(payload.id), "output": payload.output}
    except Exception as e:
        logging.error(f"Error retrieving payload: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
