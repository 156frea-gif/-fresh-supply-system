from sqlalchemy.orm import Session
from models.shipment import ShipmentModel
from models.product import ProductModel
from schemas.shipment_schema import ShipmentCreate
from fastapi import HTTPException, status

class LogisticService:
    @staticmethod
    def create_shipment(db: Session, shipment_data: ShipmentCreate):
        product = db.query(ProductModel).filter(ProductModel.id == shipment_data.product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="المنتج المطلوب للشحن غير موجود.")
        if product.quantity < shipment_data.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="الكمية المتوفرة في المخزون غير كافية لإتمام الشحنة."
            )
        
        existing_tracking = db.query(ShipmentModel).filter(
            ShipmentModel.tracking_number == shipment_data.tracking_number
        ).first()
        if existing_tracking:
            raise HTTPException(status_code=400, detail="رقم التتبع مستخدم مسبقاً.")

        product.quantity -= shipment_data.quantity

        new_shipment = ShipmentModel(
            tracking_number=shipment_data.tracking_number,
            product_id=shipment_data.product_id,
            quantity=shipment_data.quantity,
            destination=shipment_data.destination
        )
        db.add(new_shipment)
        db.commit()
        db.refresh(new_shipment)
        return new_shipment

    @staticmethod
    def update_shipment_status(db: Session, tracking_number: str, new_status: str):
        shipment = db.query(ShipmentModel).filter(ShipmentModel.tracking_number == tracking_number).first()
        if not shipment:
            raise HTTPException(status_code=404, detail="رقم الشحنة غير موجود.")
        if new_status not in ["IN_TRANSIT", "DELIVERED", "DAMAGED"]:
            raise HTTPException(status_code=400, detail="حالة الشحنة غير صالحة.")
        
        shipment.status = new_status
        db.commit()
        db.refresh(shipment)
        return shipment
