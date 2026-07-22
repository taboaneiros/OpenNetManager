
import pytest
from django.contrib.auth import get_user_model
from django.urls import reverse

from apps.devices.models import ClientModel, DeviceModel, EventModel, InterfaceModel, SnapshotModel


@pytest.mark.django_db
def test_dashboard_requires_authentication(client):
    response = client.get(reverse("dashboard-index"))
    assert response.status_code == 302
    assert "/auth/login/" in response.url


@pytest.mark.django_db
def test_dashboard_renders_for_authenticated_user(client):
    user = get_user_model().objects.create_user(
        username="tester",
        email="tester@example.com",
        password="secret123",
    )
    device = DeviceModel.objects.create(
        hostname="ap130-lab",
        vendor="AP130",
        model="AP130",
        firmware="2.1.0",
        serial="SER123",
        management_ip="192.168.1.20",
        status="online",
    )
    ClientModel.objects.create(
        device=device,
        mac="AA:BB:CC:DD:EE:01",
        ip="192.168.1.101",
        hostname="notebook-ti",
        signal=-50,
        rx="300M",
        tx="240M",
        is_online=True,
    )

    assert client.login(username="tester", password="secret123")
    response = client.get(reverse("dashboard-index"))

    assert response.status_code == 200
    assert "OpenNetManager" in response.content.decode()


@pytest.mark.django_db
def test_device_detail_view_renders(client):
    user = get_user_model().objects.create_user(
        username="tester3",
        email="tester3@example.com",
        password="secret123",
    )
    device = DeviceModel.objects.create(
        hostname="ap130-lab",
        vendor="AP130",
        model="AP130",
        firmware="2.1.0",
        serial="SER125",
        management_ip="192.168.1.25",
        status="online",
    )
    InterfaceModel.objects.create(device=device, name="eth0", status="up", speed="1G")
    EventModel.objects.create(
        device=device,
        severity="info",
        message="Teste de evento",
        occurred_at="2026-07-18T23:00:00Z",
    )
    SnapshotModel.objects.create(
        device=device,
        timestamp="2026-07-18T23:00:00Z",
        duration=1.0,
        payload={"summary": {"online_clients": 0, "offline_clients": 0}},
    )

    client.login(username="tester3", password="secret123")
    response = client.get(reverse("dashboard-device-detail", args=[device.id]))

    assert response.status_code == 200
    assert "Histórico de snapshots" in response.content.decode()
