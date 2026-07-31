from __future__ import annotations

from core.drivers.base import BaseDriver
from core.ssh.menu_executor import GWNMenuExecutor


class GWN7600Driver(BaseDriver):
    """Driver for Grandstream GWN7600 WiFi Access Points."""

    # Menu options
    MENU_STATUS = "1"       # System status and info
    MENU_CLIENTS = "4"      # Connected clients
    MENU_RADIO = "10"       # Radio configuration

    def __init__(self, executor: GWNMenuExecutor) -> None:
        # Store as menu_executor to distinguish from SSHExecutor
        self.menu_executor = executor
        # Also set executor for BaseDriver compatibility
        self.executor = executor

    def execute(self, command: str) -> str:
        """Execute a menu navigation (compatibility with BaseDriver)."""
        return self.menu_executor.navigate_to(command)

    def collect_system(self) -> str:
        """Collect system information from menu option 1 (Status)."""
        result = self.menu_executor.navigate_to(self.MENU_STATUS)
        self.menu_executor.go_back()  # Return to main menu
        return result

    def collect_version(self) -> str:
        """Collect version information (same as system for GWN)."""
        # Version info is included in the status menu
        return self.collect_system()

    def collect_interfaces(self) -> str:
        """Collect radio/interface configuration from menu option 10."""
        result = self.menu_executor.navigate_to(self.MENU_RADIO)
        self.menu_executor.go_back()  # Return to main menu
        return result

    def collect_stations(self) -> str:
        """Collect connected clients from menu option 4."""
        result = self.menu_executor.navigate_to(self.MENU_CLIENTS)
        self.menu_executor.go_back()  # Return to main menu
        return result

    def collect_all(self) -> dict[str, str]:
        """Collect all data from the device."""
        return {
            "system": self.collect_system(),
            "version": self.collect_version(),
            "interfaces": self.collect_interfaces(),
            "stations": self.collect_stations(),
        }

    def go_back(self) -> str:
        """Return to previous menu."""
        return self.menu_executor.go_back()