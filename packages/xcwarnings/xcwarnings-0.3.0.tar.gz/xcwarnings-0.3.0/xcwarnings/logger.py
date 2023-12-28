"""Custom logger."""

import enum
import logging
import os
import sys

from typing import ClassVar


class TerminalFormat(enum.Enum):
    """Bash terminal format codes."""

    RED: ClassVar[str] = "\033[91m"
    YELLOW: ClassVar[str] = "\033[93m"

    BACKGROUND_RED: ClassVar[str] = "\33[41m"

    END: ClassVar[str] = "\033[0m"


class ColoredFormatter(logging.Formatter):
    """Colorizes the logging level when it is used in the format string."""

    MAPPING: ClassVar[dict[str, TerminalFormat]] = {
        "WARNING": TerminalFormat.YELLOW,
        "ERROR": TerminalFormat.RED,
        "CRITICAL": TerminalFormat.BACKGROUND_RED,
    }

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record

        :param record: The log record to format

        :returns: The formatted record
        """

        pre_formatted = super().format(record)

        if not sys.stdout.isatty():
            return pre_formatted

        color = ColoredFormatter.MAPPING.get(record.levelname)

        if color is None:
            return pre_formatted

        return f"{color.value}{pre_formatted}{TerminalFormat.END.value}"


def _configure(logger: logging.Logger, with_decorators: bool = True) -> None:
    """Configure the logger.

    :param logger: The logger to configure
    :param filename: The file to write the log contents out to
    :param with_decorators: If False only the message will be printed (no timestamp or level name)
    """

    # Base logging level. Handlers can set their own ones
    logger.setLevel(logging.DEBUG)
    # Do not pass logging messages to the handlers of ancestor loggers
    logger.propagate = False

    if with_decorators:
        format_string = (
            "[%(asctime)s.%(msecs)03d] [%(name)s] [%(levelname)s] %(message)s"
        )
    else:
        format_string = "%(message)s"

    colored_formatter = ColoredFormatter(format_string)
    colored_formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    formatter = logging.Formatter(format_string)
    formatter.datefmt = "%Y-%m-%d %H:%M:%S"

    stream_handler = logging.StreamHandler()

    if os.environ.get("SYSTEM_DEBUG") == "true":
        stream_handler.setLevel(logging.DEBUG)
    else:
        stream_handler.setLevel(logging.INFO)

    stream_handler.setFormatter(colored_formatter)

    logger.addHandler(stream_handler)


def create_logger(identifier: str, with_decorators: bool = True) -> logging.Logger:
    """Create a logger for the stage (all other loggers will be children).

    :param stage_id: The ID of the stage logger
    :param with_decorators: If False only the message will be printed (no timestamp or level name)

    :returns: The stage logger
    """

    logger = logging.getLogger(identifier)

    _configure(logger, with_decorators)

    return logger
