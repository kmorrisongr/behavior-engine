import logging
from enum import Enum, auto
from uuid import uuid4

import structlog


class QuietType(Enum):
    QUIET = auto()


def get_logger(
    log: logging.Logger | structlog.BoundLogger | None | QuietType,
) -> logging.Logger | structlog.BoundLogger:
    """
    Get a logger.

    Args:
        log: Possibly a logger, None, or `QuietType.QUIET`.

    Returns:
        The provided logger if it exists, a null logger if `QuietType.QUIET`, or the structlog
        logger if None.
    """
    if log is QuietType.QUIET:
        return get_null_logger()
    elif log is not None:
        return log
    return structlog.get_logger()  # type: ignore[no-any-return,misc]


def get_null_logger() -> logging.Logger:
    """
    Get a unique logger that does nothing.

    Returns:
        A logger that uses a NullHandler.
    """
    logger = logging.getLogger(str(uuid4()))

    null_handler = logging.NullHandler()
    logger.addHandler(null_handler)
    return logger
