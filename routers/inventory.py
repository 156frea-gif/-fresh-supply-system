from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from core.database import get_db
from schemas.product_schema import ProductCreate, ProductResponse
from services.inventory_service import InventoryService

router = APIRouter()

@router.post("/products", response_model=ProductResponse)
def add_product(product: ProductCreate, role: str = Header(default="worker"), db: Session = Depends(get_db)):
    if role not in ["admin", "manager"]:
        raise HTTPException(status_code=403, detail="غير مصرح لك: إضافة المنتجات تتطلب صلاحية admin أو manager.")
    return InventoryService.register_product(db, product)

@router.post("/products/{product_id}/audit-temp")
def check_temperature(product_id: int, current_temp: float, db: Session = Depends(get_db)):
    return InventoryService.audit_storage_conditions(db, product_id, current_temp)

@router.get("/spoilage-report")
def get_spoilage_report(db: Session = Depends(get_db)):
    return InventoryService.generate_spoilage_report(db)
