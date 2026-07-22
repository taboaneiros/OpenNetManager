
from __future__ import annotations

from typing import Optional

import paramiko

from core.ssh.config import SSHConfig
from core.ssh.exceptions import SSHConnectionError


class SSHConnection:
    """Manage a low-level SSH shell connection."""

    def __init__(self, config: SSHConfig) -> None:
        self.config = config
        self._client: Optional[paramiko.SSHClient] = None
        self._shell = None

    def connect(self) -> None:
        """Open SSH connection and invoke interactive shell."""
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            client.connect(
                hostname=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                timeout=self.config.timeout,
                look_for_keys=False,
                allow_agent=False,
            )
            shell = client.invoke_shell()
            shell.settimeout(self.config.timeout)
            self._client = client
            self._shell = shell
        except Exception as exc:
            raise SSHConnectionError(str(exc)) from exc

    def ensure_connected(self) -> None:
        """Ensure the SSH shell is connected."""
        if self._client is None or self._shell is None:
            self.connect()

    @property
    def shell(self):
        """Return interactive shell."""
        self.ensure_connected()
        return self._shell

    def close(self) -> None:
        """Close shell and client."""
        if self._shell is not None:
            self._shell.close()
        if self._client is not None:
            self._client.close()
        self._shell = None
        self._client = None
