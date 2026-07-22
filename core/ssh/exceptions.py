
class SSHError(Exception):
    """Base SSH exception."""


class SSHConnectionError(SSHError):
    """Raised when an SSH connection fails."""


class SSHExecutionError(SSHError):
    """Raised when command execution fails."""
