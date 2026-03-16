class GameSessionNotFoundError(Exception):
    """Raised when a game session is not found."""


class InvalidDiceTypeError(Exception):
    """Raised when an invalid dice type is specified."""


class InvalidGameModeError(Exception):
    """Raised when an invalid game mode is specified."""


class HistoryExportError(Exception):
    """Raised when there is an error exporting history."""


# "Internal server error"
class InternalServerError(Exception):
    """Raised when an unexpected error occurs in the server."""
