import pytest

from core.domain.entities import Client, Snapshot
from core.repositories.clients import ClientRepository
from core.repositories.devices import DeviceRepository
from core.repositories.snapshots import SnapshotRepository


@pytest.mark.django_db
def test_device_repository_to_domain(device):
    repo = DeviceRepository()
    entity = repo.to_domain(device)
    assert entity.hostname == "ap-lab-01"


@pytest.mark.django_db
def test_client_repository_replace_for_device(device):
    repo = ClientRepository()
    repo.replace_for_device(
        device,
        [
            Client(
                mac="AA:BB:CC",
                ip="10.0.0.2",
                hostname="cli",
                signal=-60,
                rx="100M",
                tx="90M",
                last_seen=None,
                is_online=True,
            )
        ],
    )
    assert device.clients.count() == 1


@pytest.mark.django_db
def test_snapshot_repository_create(device):
    repo = SnapshotRepository()
    snapshot = Snapshot(
        device_id=device.id,
        timestamp=device.created_at,
        payload={"ok": True},
        duration=1.2,
    )
    created = repo.create(snapshot)
    assert created.payload["ok"] is True
