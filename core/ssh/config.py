
from dataclasses import dataclass


@dataclass(frozen=True)
class SSHConfig:
    """SSH connection configuration."""

    host: str
    username: str
    password: str
    port: int = 22
    timeout: int = 10
    retries: int = 2
    encoding: str = "utf-8"
    prompt_suffix: str = "#"
    more_patterns: tuple[str, ...] = ("--More--", "More:", "-- More --")
    read_chunk_size: int = 4096
