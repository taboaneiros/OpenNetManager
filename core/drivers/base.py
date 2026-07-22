
from __future__ import annotations

from abc import ABC, abstractmethod

from core.ssh.executor import SSHExecutor


class BaseDriver(ABC):
    """Base driver for network devices."""

    def __init__(self, executor: SSHExecutor) -> None:
        self.executor = executor

    @abstractmethod
    def collect_system(self) -> str:
        """Collect raw system information."""

    @abstractmethod
    def collect_interfaces(self) -> str:
        """Collect raw interface information."""

    @abstractmethod
    def collect_stations(self) -> str:
        """Collect raw station information."""

    @abstractmethod
    def collect_version(self) -> str:
        """Collect raw version information."""
