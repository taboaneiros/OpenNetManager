from __future__ import annotations

from core.domain.entities import SystemData


class SystemParser:
    """Parse system/version output into system entity."""

    def parse(self, raw_text: str) -> SystemData:
        """Extract hostname, model, firmware, serial and uptime."""
        hostname = ""
        serial = ""
        firmware = ""
        model = ""
        uptime = ""

        for line in raw_text.splitlines():
            row = line.strip()
            if ":" not in row:
                continue

            key, value = [part.strip() for part in row.split(":", 1)]
            lowered = key.lower()

            if lowered in {"hostname", "host name", "ap name", "device name"}:
                hostname = value
            elif lowered in {"serial", "serial number"}:
                serial = value
            elif lowered in {"firmware", "firmware version"}:
                firmware = value
            elif lowered in {"model", "product", "platform"}:
                model = value
            elif lowered == "uptime":
                uptime = value
            elif lowered == "version" and not firmware:
                firmware = value

        return SystemData(
            hostname=hostname,
            serial=serial,
            firmware=firmware,
            model=model,
            uptime=uptime,
        )