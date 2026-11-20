from fastapi.testclient import TestClient
from main import app
import datetime

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200

def test_add_product_unauthorized_role():
    # اختبار مدخلات خاطئة: عامل يحاول إضافة منتج بدون صلاحية
    response = client.post(
        "/api/inventory/products",
        headers={"role": "worker"},
        json={
            "sku": "MILK-001",
            "name": "حليب طازج",
            "category": "ألبان",
            "quantity": 50,
            "max_temperature": 4.0,
            "expiry_date": (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat()
        }
    )
    assert response.status_code == 403

def test_add_product_success_and_audit_temp():
    # إضافة منتج بصلاحية مدير ثم فحص الحرارة عند تجاوز الحد
    expiry = (datetime.datetime.utcnow() + datetime.timedelta(days=10)).isoformat()
    res = client.post(
        "/api/inventory/products",
        headers={"role": "admin"},
        json={
            "sku": "CHEESE-99",
            "name": "جبن أبيض",
            "category": "ألبان",
            "quantity": 30,
            "max_temperature": 5.0,
            "expiry_date": expiry
        }
    )
    assert res.status_code == 200
    product_id = res.json()["id"]

    # فحص حرارة مرتفعة (تحذير ALERT)
    audit = client.post(f"/api/inventory/products/{product_id}/audit-temp?current_temp=9.5")
    assert audit.status_code == 200
    assert audit.json()["status"] == "ALERT"
