from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from core.database import Base
import datetime

class ShipmentModel(Base):
    __tablename__ = "shipments"

    id = Column(Integer, primary_key=True, index=True)
    tracking_number = Column(String, unique=True, index=True, nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    destination = Column(String, nullable=False)
    status = Column(String, default="IN_TRANSIT")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
