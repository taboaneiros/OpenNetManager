from apps.devices.models import DeviceModel, SnapshotModel
from core.domain.entities import Snapshot


class SnapshotRepository:
    """Repository for snapshot persistence."""

    def create(self, snapshot: Snapshot) -> SnapshotModel:
        """Persist a snapshot."""
        device = DeviceModel.objects.get(pk=snapshot.device_id)
        return SnapshotModel.objects.create(
            device=device,
            timestamp=snapshot.timestamp,
            payload=snapshot.payload,
            duration=snapshot.duration,
        )

    def latest(self) -> SnapshotModel | None:
        """Return latest snapshot."""
        return SnapshotModel.objects.first()
