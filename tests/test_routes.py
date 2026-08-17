from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_dashboard_route():
    response = client.get("/")
    assert response.status_code == 200
    assert b"Dashboard" in response.content

def test_upload_route():
    response = client.get("/upload")
    assert response.status_code == 200

def test_classify_route():
    response = client.get("/classify")
    assert response.status_code == 200

def test_send_route():
    response = client.get("/send")
    assert response.status_code == 200

def test_report_route():
    response = client.get("/report")
    assert response.status_code == 200

def test_settings_route():
    response = client.get("/settings")
    assert response.status_code == 200
