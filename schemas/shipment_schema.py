from pydantic import BaseModel, Field
from datetime import datetime

class ShipmentCreate(BaseModel):
    tracking_number: str
    product_id: int
    quantity: int = Field(..., gt=0, description="كمية الشحنة يجب أن تكون أكبر من 0")
    destination: str

class ShipmentResponse(ShipmentCreate):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
