import pytest
from django.contrib.auth.models import User

from apps.devices.models import DeviceModel


@pytest.fixture
def user(db):
    return User.objects.create_user(username="admin", password="admin123")


@pytest.fixture
def device(db):
    return DeviceModel.objects.create(
        hostname="ap-lab-01",
        vendor="AP130",
        model="AP130",
        firmware="1.0.0",
        serial="SER123",
        management_ip="192.168.1.10",
        status="unknown",
        ssh_username="admin",
        ssh_password="password",
    )
