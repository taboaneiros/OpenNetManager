from __future__ import annotations

import time

from core.ssh.exceptions import SSHExecutionError


class SSHExecutor:
    """Execute commands over an interactive SSH shell."""

    MORE_MARKERS = ("--More--", "More:", "(more)")

    def __init__(self, connection) -> None:
        self.connection = connection

    def execute(self, command: str, timeout: int | None = None) -> str:
        shell = self.connection.shell
        if shell is None:
            raise SSHExecutionError("Shell not initialized.")

        effective_timeout = timeout or getattr(
            getattr(self.connection, "config", None),
            "timeout",
            15,
        )

        shell.send(f"{command}\n")

        chunks: list[str] = []
        started = time.monotonic()

        while time.monotonic() - started <= effective_timeout:
            if shell.recv_ready():
                data = shell.recv(65535).decode("utf-8", errors="ignore")
                if data:
                    chunks.append(data)

                    if self._has_more_prompt(data):
                        shell.send(" ")
                        continue

                    if self._looks_finished(data):
                        break

            time.sleep(0.05)

        output = "".join(chunks).strip()
        if not output:
            raise SSHExecutionError("Timed out waiting for command output.")

        return self._clean_output(command, output)

    def _has_more_prompt(self, text: str) -> bool:
        return any(marker in text for marker in self.MORE_MARKERS)

    def _looks_finished(self, text: str) -> bool:
        stripped = text.rstrip()
        return stripped.endswith("#") or stripped.endswith(">")

    def _clean_output(self, command: str, output: str) -> str:
        text = output.replace("\r", "")

        for marker in self.MORE_MARKERS:
            text = text.replace(marker, "")

        lines = text.splitlines()

        cleaned: list[str] = []
        command_removed = False

        for line in lines:
            stripped = line.strip()

            if not command_removed and stripped == command:
                command_removed = True
                continue

            if stripped.endswith("#") or stripped.endswith(">"):
                continue

            cleaned.append(line.rstrip())

        return "\n".join(cleaned).strip()