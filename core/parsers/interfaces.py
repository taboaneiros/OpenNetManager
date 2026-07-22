from __future__ import annotations

import re

from core.domain.entities import InterfaceData


class InterfaceParser:
    """Parse interface output into interface entities."""

    ROW_RE = re.compile(
        r"^(?P<name>\S+)\s+"
        r"(?P<mac>[0-9a-f:]+)\s+"
        r"(?P<mode>\S+)\s+"
        r"(?P<state>[UD])\s+"
        r"(?P<channel>\S+)",
        re.IGNORECASE,
    )

    def parse(self, raw_text: str) -> list[InterfaceData]:
        """Parse AP130 interface table."""
        interfaces: list[InterfaceData] = []
        seen: set[str] = set()

        for line in raw_text.splitlines():
            row = line.strip()
            if not row:
                continue
            if row.startswith("State=") or row.startswith("Radio="):
                continue
            if row.startswith("Name ") or row.startswith("--------"):
                continue

            item = self._parse_ap130_row(row)
            if not item:
                continue
            if item.name in seen:
                continue

            seen.add(item.name)
            interfaces.append(item)

        return interfaces

    def _parse_ap130_row(self, row: str) -> InterfaceData | None:
        """Parse one AP130 table row."""
        match = self.ROW_RE.match(row)
        if not match:
            return None

        name = match.group("name")
        state = match.group("state").upper()
        channel = match.group("channel")

        status = "up" if state == "U" else "down"
        speed = self._extract_width(channel)

        return InterfaceData(
            name=name,
            status=status,
            speed=speed,
        )

    def _extract_width(self, channel: str) -> str:
        """Extract width from channel description."""
        match = re.search(r"\((\d+MHz)\)", channel, re.IGNORECASE)
        if match:
            return match.group(1)
        return "-"