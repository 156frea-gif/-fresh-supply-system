from fastapi.testclient import TestClient
from main import app
import datetime

client = TestClient(app)

def test_create_shipment_invalid_product():
    # اختبار مدخلات خاطئة: شحنة لمنتج غير موجود
    response = client.post(
        "/api/shipments/",
        json={
            "tracking_number": "TRK-ERR-1",
            "product_id": 99999,
            "quantity": 5,
            "destination": "الدمام"
        }
    )
    assert response.status_code == 404

def test_create_shipment_exceeds_stock():
    # إنشاء منتج بكمية 10 ثم محاولة شحن 50 (مدخلات خاطئة)
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).isoformat()
    prod = client.post(
        "/api/inventory/products",
        headers={"role": "manager"},
        json={
            "sku": "APPLE-55",
            "name": "تفاح أحمر",
            "category": "فواكه",
            "quantity": 10,
            "max_temperature": 6.0,
            "expiry_date": expiry
        }
    ).json()

    ship = client.post(
        "/api/shipments/",
        json={
            "tracking_number": "TRK-OVER-1",
            "product_id": prod["id"],
            "quantity": 50,
            "destination": "الرياض"
        }
    )
    assert ship.status_code == 400

def test_create_and_track_shipment_success():
    # إنشاء شحنة ناجحة وتحديث حالتها
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=5)).isoformat()
    prod = client.post(
        "/api/inventory/products",
        headers={"role": "admin"},
        json={
            "sku": "TOMATO-77",
            "name": "طماطم طازجة",
            "category": "خضروات",
            "quantity": 100,
            "max_temperature": 8.0,
            "expiry_date": expiry
        }
    ).json()

    ship = client.post(
        "/api/shipments/",
        json={
            "tracking_number": "TRK-OK-100",
            "product_id": prod["id"],
            "quantity": 20,
            "destination": "جدة"
        }
    )
    assert ship.status_code == 200
    assert ship.json()["status"] == "IN_TRANSIT"

    update = client.patch("/api/shipments/TRK-OK-100/status?status=DELIVERED")
    assert update.status_code == 200
    assert update.json()["status"] == "DELIVERED"
