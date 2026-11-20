from pydantic import BaseModel, Field
from datetime import datetime

class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    quantity: int = Field(..., ge=0, description="الكمية يجب أن تكون 0 أو أكثر")
    max_temperature: float
    expiry_date: datetime

class ProductResponse(ProductCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
