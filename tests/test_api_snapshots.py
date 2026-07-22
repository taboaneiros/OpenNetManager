
import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from apps.devices.models import DeviceModel, SnapshotModel


@pytest.mark.django_db
def test_snapshots_endpoint_returns_data():
    user = get_user_model().objects.create_user(
        username="apitester",
        email="api@example.com",
        password="secret123",
    )
    device = DeviceModel.objects.create(
        hostname="ap130-lab",
        vendor="AP130",
        model="AP130",
        firmware="2.1.0",
        serial="SER900",
        management_ip="192.168.1.90",
        status="online",
    )
    SnapshotModel.objects.create(
        device=device,
        timestamp="2026-07-18T23:00:00Z",
        duration=1.3,
        payload={"summary": {"online_clients": 1, "offline_clients": 0}},
    )

    client = APIClient()
    client.login(username="apitester", password="secret123")
    response = client.get("/api/snapshots/")

    assert response.status_code == 200
