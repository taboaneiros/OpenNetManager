class SSHExecutionError(Exception):
    """Raised when SSH command execution fails."""


class ParserError(Exception):
    """Raised when parsing fails."""


class DriverError(Exception):
    """Raised when driver execution fails."""


class RepositoryError(Exception):
    """Raised when repository operation fails."""
