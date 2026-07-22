import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
def test_devices_endpoint_requires_auth(device):
    client = APIClient()
    response = client.get("/api/devices/")
    assert response.status_code == 403


@pytest.mark.django_db
def test_devices_endpoint_returns_data(user, device):
    client = APIClient()
    client.login(username="admin", password="admin123")
    response = client.get("/api/devices/")
    assert response.status_code == 200
    assert response.json()[0]["hostname"] == "ap-lab-01"
