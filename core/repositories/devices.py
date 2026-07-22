from apps.devices.models import DeviceModel
from core.domain.entities import Device


class DeviceRepository:
    """Repository for device persistence."""

    def list_all(self):
        """Return all device models."""
        return DeviceModel.objects.all()

    def get_by_id(self, device_id: int) -> DeviceModel:
        """Return a device model by identifier."""
        return DeviceModel.objects.get(pk=device_id)

    def to_domain(self, model: DeviceModel) -> Device:
        """Convert ORM model to domain object."""
        return Device(
            id=model.id,
            hostname=model.hostname,
            vendor=model.vendor,
            model=model.model,
            firmware=model.firmware,
            serial=model.serial,
            management_ip=model.management_ip,
            status=model.status,
        )

    def update_system(self, device_id: int, firmware: str, serial: str, status: str) -> None:
        """Update device system fields."""
        DeviceModel.objects.filter(pk=device_id).update(
            firmware=firmware,
            serial=serial,
            status=status,
        )
