
import pytest

from apps.devices.models import ClientModel, DeviceModel, InterfaceModel, SnapshotModel
from core.services.collector import CollectorService


@pytest.mark.django_db
def test_collect_device_persists_snapshot_clients_interfaces():
    device = DeviceModel.objects.create(
        hostname="ap130-lab",
        vendor="AP130",
        model="AP130",
        firmware="2.1.0",
        serial="SER555",
        management_ip="192.168.1.55",
        status="online",
        ssh_username="admin",
        ssh_password="changeme",
    )

    service = CollectorService()
    result = service.collect_device(device.id)

    assert SnapshotModel.objects.filter(device=device).count() == 1
    assert ClientModel.objects.filter(device=device).count() >= 1
    assert InterfaceModel.objects.filter(device=device).count() >= 1
    assert result["device_id"] == device.id
