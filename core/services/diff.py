
from __future__ import annotations

from dataclasses import asdict

from core.domain.entities import ClientData


class SnapshotDiffService:
    """Generate diff between previous and current client state."""

    def build_client_diff(
        self,
        previous_clients: list[ClientData],
        current_clients: list[ClientData],
    ) -> dict[str, list[dict]]:
        previous_map = {client.mac.lower(): client for client in previous_clients}
        current_map = {client.mac.lower(): client for client in current_clients}

        joined: list[dict] = []
        left: list[dict] = []
        changed: list[dict] = []

        for mac, client in current_map.items():
            if mac not in previous_map:
                joined.append(asdict(client))
                continue

            before = previous_map[mac]
            delta = self._client_change(before, client)
            if delta:
                changed.append(delta)

        for mac, client in previous_map.items():
            if mac not in current_map:
                left.append(asdict(client))

        return {
            "joined": joined,
            "left": left,
            "changed": changed,
        }

    def _client_change(self, before: ClientData, after: ClientData) -> dict | None:
        changes: dict[str, dict] = {}

        if before.ip != after.ip:
            changes["ip"] = {"before": before.ip, "after": after.ip}
        if before.hostname != after.hostname:
            changes["hostname"] = {"before": before.hostname, "after": after.hostname}
        if before.signal != after.signal:
            changes["signal"] = {"before": before.signal, "after": after.signal}
        if before.rx != after.rx:
            changes["rx"] = {"before": before.rx, "after": after.rx}
        if before.tx != after.tx:
            changes["tx"] = {"before": before.tx, "after": after.tx}

        if not changes:
            return None

        return {
            "mac": after.mac,
            "hostname": after.hostname,
            "changes": changes,
        }
