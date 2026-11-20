from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.shipment_schema import ShipmentCreate, ShipmentResponse
from services.logistic_service import LogisticService

router = APIRouter()

@router.post("/", response_model=ShipmentResponse)
def create_shipment(shipment: ShipmentCreate, db: Session = Depends(get_db)):
    return LogisticService.create_shipment(db, shipment)

@router.patch("/{tracking_number}/status", response_model=ShipmentResponse)
def update_status(tracking_number: str, status: str, db: Session = Depends(get_db)):
    return LogisticService.update_shipment_status(db, tracking_number, status)
