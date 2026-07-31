from __future__ import annotations

import re
import time

from core.ssh.exceptions import SSHExecutionError


class GWNMenuExecutor:
    """Execute navigation in Grandstream interactive menu systems."""

    MENU_TIMEOUT = 3  # seconds to wait for menu to load
    BACK_COMMAND = "x"
    MENU_HEADER_PATTERN = re.compile(r"GWN\d+\([^)]+\)")

    def __init__(self, connection) -> None:
        self.connection = connection
        self.shell = connection.shell

    def navigate_to(self, menu_option: str, timeout: int | None = None) -> str:
        """Navigate to a menu option and return the content."""
        if self.shell is None:
            raise SSHExecutionError("Shell not initialized.")

        effective_timeout = timeout or self.MENU_TIMEOUT

        # Send menu option
        self.shell.send(f"{menu_option}\n")

        # Wait for menu content to load
        return self._read_menu_content(effective_timeout)

    def go_back(self, timeout: int | None = None) -> str:
        """Return to previous menu."""
        if self.shell is None:
            raise SSHExecutionError("Shell not initialized.")

        effective_timeout = timeout or self.MENU_TIMEOUT
        self.shell.send(f"{self.BACK_COMMAND}\n")
        return self._read_menu_content(effective_timeout)

    def _read_menu_content(self, timeout: int) -> str:
        """Read menu content until it stabilizes."""
        chunks: list[str] = []
        started = time.monotonic()
        last_data_time = started

        while time.monotonic() - started <= timeout:
            if self.shell.recv_ready():
                data = self.shell.recv(65535).decode("utf-8", errors="ignore")
                if data:
                    chunks.append(data)
                    last_data_time = time.monotonic()

                    # Check if we've reached a stable state
                    if self._is_menu_complete(data):
                        # Small delay to ensure no more data is coming
                        time.sleep(0.2)
                        if not self.shell.recv_ready():
                            break
                else:
                    time.sleep(0.05)
            else:
                # If we got data recently, wait a bit more
                if chunks and time.monotonic() - last_data_time < 0.5:
                    time.sleep(0.05)
                else:
                    time.sleep(0.05)

        output = "".join(chunks).strip()
        if not output:
            raise SSHExecutionError("Timed out waiting for menu content.")

        return self._clean_output(output)

    def _is_menu_complete(self, text: str) -> bool:
        """Check if menu content appears complete."""
        # Menu is complete when we see the back option or select prompt
        indicators = [
            "[x] Back",
            "[x] Exit",
            "Select by pressing",
            "[z] Exit List",
        ]
        return any(indicator in text for indicator in indicators)

    def _clean_output(self, output: str) -> str:
        """Clean and normalize menu output."""
        # Remove carriage returns
        text = output.replace("\r", "")

        # Remove ANSI escape sequences
        ansi_escape = re.compile(r"\x1b\[[0-9;]*[a-zA-Z]")
        text = ansi_escape.sub("", text)

        # Split into lines and clean
        lines = text.splitlines()
        cleaned: list[str] = []

        for line in lines:
            stripped = line.rstrip()
            # Skip empty lines at the beginning
            if not cleaned and not stripped:
                continue
            cleaned.append(stripped)

        # Remove trailing empty lines
        while cleaned and not cleaned[-1]:
            cleaned.pop()

        return "\n".join(cleaned)

    def wait_for_main_menu(self, timeout: int = 5) -> str:
        """Wait for the main menu to appear after connection."""
        if self.shell is None:
            raise SSHExecutionError("Shell not initialized.")

        chunks: list[str] = []
        started = time.monotonic()

        while time.monotonic() - started <= timeout:
            if self.shell.recv_ready():
                data = self.shell.recv(65535).decode("utf-8", errors="ignore")
                if data:
                    chunks.append(data)

                    # Check if main menu appeared
                    if "Main Menu" in data or "[1] Status" in data:
                        time.sleep(0.3)
                        break

            time.sleep(0.05)

        output = "".join(chunks).strip()
        return self._clean_output(output)