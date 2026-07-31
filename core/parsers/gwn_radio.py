from __future__ import annotations

import re

from core.domain.entities import InterfaceData


class GWNRadioParser:
    """Parse GWN7600 radio configuration output."""

    # Pattern for radio configuration lines:
    # [5] 2g4   Channel Width: 40MHz       Short Guard Interval: Enabled
    # [6] 5g  Channel Width: 80MHz       Short Guard Interval: Enabled

    RADIO_HEADER_RE = re.compile(
        r"\[(\d+)\]\s+"
        r"(2g4|5g)\s+"
        r"Channel Width:\s*(\S+)"
    )

    CHANNEL_RE = re.compile(r"Channel:\s*(\S+)")
    POWER_RE = re.compile(r"Radio Power:\s*(.+?)(?:\s{2,}|$)")

    def parse(self, raw_text: str) -> list[InterfaceData]:
        """Parse radio interfaces from configuration output."""
        interfaces: list[InterfaceData] = []

        current_radio = None
        current_config: dict = {}

        for line in raw_text.splitlines():
            line = line.strip()
            if not line:
                continue

            # Check for radio header line FIRST (before skip check)
            header_match = self.RADIO_HEADER_RE.search(line)
            if header_match:
                # Save previous radio if exists
                if current_radio and current_config:
                    interfaces.append(self._build_interface(current_radio, current_config))

                current_radio = header_match.group(2)  # 2g4 or 5g
                current_config = {
                    "channel_width": header_match.group(3),
                }

                # Extract additional fields from the same line
                channel_match = self.CHANNEL_RE.search(line)
                if channel_match:
                    current_config["channel"] = channel_match.group(1)

                continue  # Processed header, move to next line

            # Skip header/footer lines (only if NOT a radio header)
            if self._is_skip_line(line):
                continue

            # Check for channel on continuation line
            if current_radio:
                channel_match = self.CHANNEL_RE.search(line)
                if channel_match:
                    current_config["channel"] = channel_match.group(1)

                power_match = self.POWER_RE.search(line)
                if power_match:
                    current_config["power"] = power_match.group(1).strip()

        # Save last radio
        if current_radio and current_config:
            interfaces.append(self._build_interface(current_radio, current_config))

        return interfaces

    def _is_skip_line(self, line: str) -> bool:
        """Check if line should be skipped."""
        skip_markers = [
            "GWN",
            "Radio Configuration",
            "[x] Back",
            "Edit an option",
            "Select by pressing",
            "Band Steering",
            "Airtime Fairness",
            "Beacon Interval",
            "Short Guard Interval",
            "Allow Legacy",
            "Minimum RSSI",
            "Minimum Access Rate",
        ]
        return any(marker in line for marker in skip_markers)

    def _build_interface(self, radio: str, config: dict) -> InterfaceData:
        """Build InterfaceData from radio configuration."""
        name = f"wlan-{radio}"
        channel = config.get("channel", "unknown")
        width = config.get("channel_width", "")
        power = config.get("power", "")

        # Build speed string with channel info
        speed_parts = []
        if width:
            speed_parts.append(width)
        if channel and channel != "auto":
            speed_parts.append(f"ch{channel}")
        if power:
            speed_parts.append(power)

        speed = " ".join(speed_parts) if speed_parts else "auto"

        # Status is derived from power setting
        status = "up" if power and "disabled" not in power.lower() else "down"

        return InterfaceData(
            name=name,
            status=status,
            speed=speed,
        )

    def parse_band_info(self, raw_text: str) -> dict:
        """Parse detailed band information."""
        bands: dict = {}

        for line in raw_text.splitlines():
            header_match = self.RADIO_HEADER_RE.search(line)
            if header_match:
                band = header_match.group(2)  # 2g4 or 5g
                bands[band] = {
                    "channel_width": header_match.group(3),
                    "channel": None,
                    "power": None,
                }

                channel_match = self.CHANNEL_RE.search(line)
                if channel_match:
                    bands[band]["channel"] = channel_match.group(1)

        return bands