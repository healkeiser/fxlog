"""Custom logging module enabling color and log file rotation."""

# Built-in
from datetime import datetime, timedelta
import logging
import logging.handlers
import os
from pathlib import Path
import sys
from typing import Union

# Third-party
import colorama

# Constants
CRITICAL = logging.CRITICAL
FATAL = logging.FATAL
ERROR = logging.ERROR
WARNING = logging.WARNING
WARN = logging.WARN
INFO = logging.INFO
DEBUG = logging.DEBUG
NOTSET = logging.NOTSET

# Globals
_LOG_DIRECTORY = None


def set_log_directory(log_directory: Union[str, Path]) -> None:
    """Sets the log directory for the module.

    Args:
        log_directory: The directory to save the log files.

    Notes:
        This function must be called before saving logs to a file, and can
        only be called once.
    """

    global _LOG_DIRECTORY
    _LOG_DIRECTORY = Path(log_directory)


def _check_log_directory() -> None:
    """Check if the log directory is set and exists."""

    global _LOG_DIRECTORY
    if _LOG_DIRECTORY is None:
        raise ValueError(
            "Log directory is not set. Call `set_log_directory` first."
        )

    if not _LOG_DIRECTORY.is_dir():
        raise ValueError("Log directory does not exist.")


def _supports_color() -> bool:
    """Check if the terminal supports color."""

    colorama.init()

    # Check if the terminal supports color
    if sys.platform == "win32":
        return colorama.AnsiToWin32(sys.stdout).stream.isatty()
    return sys.stdout.isatty()


class FXFormatter(logging.Formatter):
    """Custom log formatter that adds color and icons to log messages based on the log
    level.

    Args:
        fmt (str): The log message format string.
        datefmt (str): The date format string.
        style (str): The format style.
        enable_color (bool): Whether to enable color logging. Note that if
            enabled but unsupported, color logging will be disabled.
            Defaults to `False`.
        enable_separator (bool): Whether to enable a separator between log
            messages. Defaults to `False`.
        enable_icon (bool): Whether to enable icons in log messages. Defaults
            to `False`.

    Attributes:
        level_colors: A dictionary mapping log levels to their respective
            color codes.
        level_icons: A dictionary mapping log levels to their respective
            icons.
        enable_color: Whether to enable color logging.
        enable_separator: Whether to enable a separator between log messages.
        enable_icon: Whether to enable icons in log messages.
    """

    def __init__(
        self,
        fmt=None,
        datefmt=None,
        style="{",
        enable_color=False,
        enable_separator=False,
    ):
        super().__init__(fmt=fmt, datefmt=datefmt, style=style)

        self.level_colors = {
            logging.DEBUG: colorama.Fore.CYAN,
            logging.INFO: colorama.Fore.GREEN,
            logging.WARNING: colorama.Fore.YELLOW,
            logging.ERROR: colorama.Fore.RED,
            logging.CRITICAL: colorama.Fore.MAGENTA,
        }

        self.enable_color = enable_color
        self.enable_separator = enable_separator

        # Disable color logging if the terminal does not support color
        if enable_color:
            if not _supports_color():
                self.enable_color = False
            else:
                colorama.just_fix_windows_console()

    def format(self, record):
        # Define widths for various parts of the log message
        width_name = 25
        width_levelname = 8

        # Format line number with padding
        record.lineno = f"{record.lineno:<4}"

        # Handle separator if enabled
        if self.enable_separator:
            separator = "-" * (57 + len(record.getMessage())) + "\n"
        else:
            separator = ""

        # Construct the log format string based on whether color is enabled
        if self.enable_color:
            log_fmt = (
                f"{separator}{{asctime}} | {{name:^{width_name}s}} | "
                f"{colorama.Fore.YELLOW}{{lineno}}{colorama.Style.RESET_ALL} | "
                f"{colorama.Style.BRIGHT}{self.level_colors.get(record.levelno, colorama.Fore.WHITE)}"
                f"{{levelname:>{width_levelname}s}}{colorama.Style.RESET_ALL} | {{message}}"
            )
        else:
            log_fmt = (
                f"{separator}{{asctime}} | {{name:^{width_name}s}} | "
                f"{{lineno}} | "
                f"{{levelname:>{width_levelname}s}} | {{message}}"
            )

        # Create a new formatter with the constructed format string
        formatter = logging.Formatter(log_fmt, style="{", datefmt="%H:%M:%S")
        return formatter.format(record)


class FXTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """Custom log file handler that rotates log files at midnight.

    Attributes:
        suffix (str): The suffix to append to the rotated log file.
    """

    def rotation_filename(self, default_name: str) -> str:
        name, ext = os.path.splitext(default_name)
        return f"{name}.{self.suffix}{ext}"


def configure_logger(
    logger_name: str,
    enable_color: bool = True,
    enable_separator: bool = False,
    save_to_file: bool = True,
) -> logging.Logger:
    """Creates a custom logger with the specified name and returns it.

    Args:
        logger_name: The name of the logger.
        enable_color: Whether to enable color logging.
            Defaults to `True`.
        enable_separator: Whether to enable a separator between log
            messages. Defaults to `False`.
        save_to_file: Whether to save logs to a file.
            Defaults to `True`.

    Returns:
        logging.Logger: The custom logger.
    """

    if save_to_file:
        _check_log_directory()

    # Check if the logger with the specified name already exists in the logger
    # dictionary
    if logger_name in logging.Logger.manager.loggerDict:
        return logging.getLogger(logger_name)

    # Formatter
    formatter = FXFormatter(
        enable_color=enable_color,
        enable_separator=enable_separator,
    )
    logger = logging.getLogger(logger_name)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)

    if save_to_file:
        # Save logs
        current_date = datetime.now().strftime("%Y-%m-%d")
        log_file_path = _LOG_DIRECTORY / f"{logger_name}.{current_date}.log"

        # Create a file handler for logging with rotation at midnight
        # (one file a day)
        file_handler = FXTimedRotatingFileHandler(
            log_file_path, "midnight", 1, 30, "utf-8"
        )
        file_handler.setFormatter(
            FXFormatter(enable_color=False, enable_separator=False)
        )
        file_handler.setLevel(logging.DEBUG)

        logger.addHandler(file_handler)

    logger.propagate = False

    return logger


def set_loggers_level(level: int) -> None:
    """Sets the logging level for all instances of loggers created by the
    `FXFormatter` class.

    Args:
        level (int): The logging level to set.
    """

    for _, logger in logging.Logger.manager.loggerDict.items():
        if isinstance(logger, logging.Logger) and logger.handlers:
            for handler in logger.handlers:
                if isinstance(handler.formatter, FXFormatter):
                    logger.setLevel(level)
                    handler.setLevel(level)


def delete_old_logs(days: int) -> None:
    """Deletes log files older than the specified number of days.

    Args:
        days: The number of days after which log files should be deleted.
    """

    _check_log_directory()

    cutoff_date = datetime.now() - timedelta(days=days)

    for log_file in _LOG_DIRECTORY.iterdir():
        if log_file.is_file():
            file_mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
            if file_mod_time < cutoff_date:
                log_file.unlink()


def clear_logs() -> None:
    """Delete all the log files."""

    _check_log_directory()

    for log_file in _LOG_DIRECTORY.iterdir():
        if log_file.is_file():
            log_file.unlink()
