from apps.devices.models import ClientModel, DeviceModel
from core.domain.entities import Client


class ClientRepository:
    """Repository for client persistence."""

    def replace_for_device(self, device: DeviceModel, clients: list[Client]) -> None:
        """Replace all clients for a device."""
        ClientModel.objects.filter(device=device).delete()
        objects = [
            ClientModel(
                device=device,
                mac=client.mac,
                ip=client.ip,
                hostname=client.hostname,
                signal=client.signal,
                rx=client.rx,
                tx=client.tx,
                last_seen=client.last_seen,
                is_online=client.is_online,
            )
            for client in clients
        ]
        ClientModel.objects.bulk_create(objects)

    def count_online(self) -> int:
        """Count online clients."""
        return ClientModel.objects.filter(is_online=True).count()

    def count_offline(self) -> int:
        """Count offline clients."""
        return ClientModel.objects.filter(is_online=False).count()
