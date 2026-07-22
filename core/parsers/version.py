from __future__ import annotations

from core.domain.entities import VersionData


class VersionParser:
    """Parse version output into version entity."""

    def parse(self, raw_text: str) -> VersionData:
        """Extract firmware version and build info."""
        firmware = ""
        build = ""

        for line in raw_text.splitlines():
            row = line.strip()
            if ":" not in row:
                continue

            key, value = [part.strip() for part in row.split(":", 1)]
            lowered = key.lower()

            if lowered in {"version", "firmware", "firmware version"}:
                firmware = value
            elif lowered in {"build", "build number", "build time"} and not build:
                build = value

        return VersionData(
            firmware=firmware,
            build=build,
        )