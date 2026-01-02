"""Custom logging module enabling color and log file rotation.

Warning:
    Enabling `save_to_file` requires calling `set_log_directory` before
    creating a logger. This can be done once inside `__init__.py`.

Examples:
    >>> import logging
    >>> from fxlog import fxlogger
    >>> _logger = fxlogger.configure_logger(__name__, save_to_file=True)
    >>> _logger.setLevel(logging.DEBUG)
    >>> _logger.debug("This is a debug message")
    >>>
    >>> # With custom message color per log call
    >>> _logger.debug("This message will be blue", color=fxlogger.BLUE)
    >>> _logger.info("This message will be red", color=fxlogger.RED)
    >>> _logger.warning("Bright yellow warning", color=fxlogger.YELLOW + fxlogger.BRIGHT)
"""

# pylint: disable=global-statement, global-variable-not-assigned

# Built-in
from datetime import datetime, timedelta
import getpass
import logging
import logging.handlers
import os
from pathlib import Path
import platform
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
_CONFIGURED_LOGGERS = set()
_SHARED_FILE_HANDLER = None
_DEFAULT_LEVEL = None  # Global default level for new loggers


def set_log_directory(log_directory: Union[str, Path]) -> None:
    """Sets the log directory for the module.

    Args:
        log_directory: The directory to save the log files.

    Notes:
        This function must be called before saving logs to a file, and can
        only be called once.
    """
    global _LOG_DIRECTORY, _SHARED_FILE_HANDLER

    if _LOG_DIRECTORY is not None:
        # Log directory already set, don't change it
        return

    _LOG_DIRECTORY = Path(log_directory)

    # Create shared file handler when log directory is set
    if _LOG_DIRECTORY.is_dir():
        _SHARED_FILE_HANDLER = _create_shared_file_handler()


def _create_shared_file_handler() -> logging.Handler:
    """Creates a shared file handler for all loggers.

    Returns:
        A TimedRotatingFileHandler that can be shared across all loggers.
    """
    current_date = datetime.now().strftime("%Y_%m_%d")
    log_directory = _LOG_DIRECTORY.joinpath(platform.node(), getpass.getuser())
    log_directory.mkdir(parents=True, exist_ok=True)

    # Single log file per day that all processes append to
    log_file = f"{current_date}.log"
    log_file_path = log_directory.joinpath(log_file)

    # Create a file handler for logging with rotation at midnight
    file_handler = FXTimedRotatingFileHandler(
        log_file_path, "midnight", 1, 30, "utf-8"
    )
    file_handler.setFormatter(
        FXFormatter(enable_color=False, enable_separator=False)
    )
    file_handler.setLevel(logging.DEBUG)

    return file_handler


def _check_log_directory() -> None:
    """Check if the log directory is set and exists."""

    global _LOG_DIRECTORY
    if _LOG_DIRECTORY is None:
        raise ValueError(
            "Log directory is not set. Call `set_log_directory` first."
        )

    if not _LOG_DIRECTORY.is_dir():
        raise ValueError(f"Log directory does not exist: '{_LOG_DIRECTORY}'.")


def _supports_color() -> bool:
    """Check if the terminal supports color, safely."""

    colorama.init()

    stream = sys.stdout

    # Handle cases where stdout is None (e.g., Cinema 4D)
    if stream is None or not hasattr(stream, "isatty"):
        return False

    try:
        if sys.platform == "win32":
            return colorama.AnsiToWin32(stream).stream.isatty()
        return stream.isatty()
    except Exception:
        return False


# Check color support once at module import
_COLOR_SUPPORTED = _supports_color()

# Colors
BLACK = colorama.Fore.BLACK if _COLOR_SUPPORTED else ""
BLUE = colorama.Fore.BLUE if _COLOR_SUPPORTED else ""
CYAN = colorama.Fore.CYAN if _COLOR_SUPPORTED else ""
GREEN = colorama.Fore.GREEN if _COLOR_SUPPORTED else ""
MAGENTA = colorama.Fore.MAGENTA if _COLOR_SUPPORTED else ""
RED = colorama.Fore.RED if _COLOR_SUPPORTED else ""
WHITE = colorama.Fore.WHITE if _COLOR_SUPPORTED else ""
YELLOW = colorama.Fore.YELLOW if _COLOR_SUPPORTED else ""
# Styles
BRIGHT = colorama.Style.BRIGHT if _COLOR_SUPPORTED else ""
DIM = colorama.Style.DIM if _COLOR_SUPPORTED else ""
RESET_ALL = colorama.Style.RESET_ALL if _COLOR_SUPPORTED else ""


class FXFormatter(logging.Formatter):
    """Custom log formatter that adds color to log messages based on the
    log level.

    Args:
        fmt (str): The log message format string.
        datefmt (str): The date format string.
        style (str): The format style.
        enable_color (bool): Whether to enable color logging. Note that if
            enabled but unsupported, color logging will be disabled.
            Defaults to `False`.
        enable_separator (bool): Whether to enable a separator between log
            messages. Defaults to `False`.

    Attributes:
        level_colors: A dictionary mapping log levels to their respective
            color codes.
        enable_color: Whether to enable color logging.
        enable_separator: Whether to enable a separator between log messages.
    """

    # Class variable to track all loggers using this formatter
    _loggers = set()

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
            if not _COLOR_SUPPORTED:
                self.enable_color = False
            else:
                colorama.just_fix_windows_console()

    def format(self, record):
        # Add logger to registry if not already tracked
        if record.name not in self._loggers:
            self._loggers.add(record.name)

        # Define widths for various parts of the log message
        width_name = 40
        width_levelname = 8

        # Add module_function attribute to the record
        record.module_function = f"{record.name}:{record.funcName}"

        # Construct the log format string based on whether color is enabled
        if self.enable_color:
            # Handle separator if enabled
            if self.enable_separator:
                separator = (
                    f"{colorama.Style.DIM}"
                    + "-" * 79
                    + f"{colorama.Style.RESET_ALL}"
                    + "\n"
                )
            else:
                separator = ""

            # Check if there's a custom color for this message
            message_color = getattr(record, "color", None)
            color_start = (
                message_color if message_color and self.enable_color else ""
            )
            color_end = (
                colorama.Style.RESET_ALL
                if message_color and self.enable_color
                else ""
            )

            # Header and message format with clear separation
            log_fmt = (
                f"{separator}"
                f"{colorama.Style.DIM}{{asctime}} {colorama.Style.RESET_ALL}"
                f"{self.level_colors.get(record.levelno, colorama.Fore.WHITE)}{{levelname:>{width_levelname}s}} {colorama.Style.RESET_ALL}{colorama.Style.DIM} {colorama.Style.RESET_ALL}"
                f"{colorama.Style.DIM}{{module_function}}:{{lineno}}{colorama.Style.RESET_ALL}\n"
                f"    {color_start}{{message}}{color_end}"
            )
        else:
            # Handle separator if enabled
            if self.enable_separator:
                separator = "-" * 79 + "\n"
            else:
                separator = ""

            # Header and message format with clear separation for non-color output
            log_fmt = (
                f"{separator}"
                f"{{asctime}} "
                f"{{levelname:>{width_levelname}s}} "
                f"{{module_function}}:{{lineno}}\n"
                f"    {{message}}"
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


class FXColorLogger(logging.Logger):
    """Custom logger class that supports color parameter in log methods."""

    def _log(
        self,
        level,
        msg,
        args,
        color=None,
        exc_info=None,
        extra=None,
        stack_info=False,
        stacklevel=1,
    ):
        """Override _log to handle color parameter."""
        if self.isEnabledFor(level):
            # Find caller with correct stack level to skip our wrapper methods
            sinfo = None
            if logging._srcfile:
                # We need to skip 2 frames: this _log method + the
                # debug/info/warning/etc method
                try:
                    fn, lno, func, sinfo = self.findCaller(
                        stack_info, stacklevel + 1
                    )
                except ValueError:
                    fn, lno, func = "(unknown file)", 0, "(unknown function)"
            else:
                fn, lno, func = "(unknown file)", 0, "(unknown function)"

            # Create a custom LogRecord that includes the color
            record = self.makeRecord(
                self.name,
                level,
                fn,
                lno,
                msg,
                args,
                exc_info,
                func,
                extra,
                sinfo,
            )
            if color:
                record.color = color
            self.handle(record)

    def debug(self, msg, *args, color=None, **kwargs):
        """Log a message with severity 'DEBUG' on this logger."""
        if self.isEnabledFor(logging.DEBUG):
            self._log(
                logging.DEBUG, msg, args, color=color, stacklevel=2, **kwargs
            )

    def info(self, msg, *args, color=None, **kwargs):
        """Log a message with severity 'INFO' on this logger."""
        if self.isEnabledFor(logging.INFO):
            self._log(
                logging.INFO, msg, args, color=color, stacklevel=2, **kwargs
            )

    def warning(self, msg, *args, color=None, **kwargs):
        """Log a message with severity 'WARNING' on this logger."""
        if self.isEnabledFor(logging.WARNING):
            self._log(
                logging.WARNING, msg, args, color=color, stacklevel=2, **kwargs
            )

    def error(self, msg, *args, color=None, **kwargs):
        """Log a message with severity 'ERROR' on this logger."""
        if self.isEnabledFor(logging.ERROR):
            self._log(
                logging.ERROR, msg, args, color=color, stacklevel=2, **kwargs
            )

    def critical(self, msg, *args, color=None, **kwargs):
        """Log a message with severity 'CRITICAL' on this logger."""
        if self.isEnabledFor(logging.CRITICAL):
            self._log(
                logging.CRITICAL, msg, args, color=color, stacklevel=2, **kwargs
            )


def configure_logger(
    logger_name: str,
    enable_color: bool = True,
    enable_separator: bool = True,
    save_to_file: bool = True,
) -> FXColorLogger:
    """Creates a custom logger with the specified name and returns it.

    Args:
        logger_name: The name of the logger.
        enable_color: Whether to enable color logging.
            Defaults to `True`.
        enable_separator: Whether to enable a separator between log
            messages. Defaults to `True`.
        save_to_file: Whether to save logs to a file.
            Defaults to `True`.

    Returns:
        FXColorLogger: The custom logger that supports color parameter.
    """

    # Check if log directory is set when save_to_file is requested
    can_save_to_file = save_to_file
    if save_to_file:
        if _LOG_DIRECTORY is None:
            print(
                f"Warning: Logger '{logger_name}' requested save_to_file=True "
                "but log directory is not set. Logs will only output to console. "
                "Call set_log_directory() to enable file logging."
            )
            can_save_to_file = False
        elif not _LOG_DIRECTORY.is_dir():
            print(
                f"Warning: Logger '{logger_name}' requested save_to_file=True "
                f"but log directory does not exist: '{_LOG_DIRECTORY}'. "
                "Logs will only output to console."
            )
            can_save_to_file = False

    # Check if the logger with the specified name already exists in the logger
    # dictionary
    if logger_name in logging.Logger.manager.loggerDict:
        existing_logger = logging.getLogger(logger_name)
        if isinstance(existing_logger, FXColorLogger):
            return existing_logger
        # If it exists but isn't a FXColorLogger, we need to replace it
        # This is a bit tricky, so we'll just continue and override

    # Set the logger class to our custom FXColorLogger
    old_logger_class = logging.getLoggerClass()
    logging.setLoggerClass(FXColorLogger)

    try:
        # Formatter
        formatter = FXFormatter(
            enable_color=enable_color,
            enable_separator=enable_separator,
        )
        logger = logging.getLogger(logger_name)
    finally:
        # Restore the original logger class
        logging.setLoggerClass(old_logger_class)

    # Console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    logger.addHandler(console_handler)

    if can_save_to_file:
        # Use the shared file handler for all loggers
        global _SHARED_FILE_HANDLER

        # Create the shared handler if it doesn't exist yet
        if _SHARED_FILE_HANDLER is None:
            _SHARED_FILE_HANDLER = _create_shared_file_handler()

        # Add the shared handler to this logger
        logger.addHandler(_SHARED_FILE_HANDLER)

    logger.propagate = False

    # Track this logger in our global set
    global _CONFIGURED_LOGGERS
    _CONFIGURED_LOGGERS.add(logger_name)

    # Apply global default level if set
    if _DEFAULT_LEVEL is not None:
        logger.setLevel(_DEFAULT_LEVEL)
        for handler in logger.handlers:
            handler.setLevel(_DEFAULT_LEVEL)

    return logger


def set_loggers_level(level: int) -> None:
    """Sets the logging level for all loggers created with configure_logger.

    This affects both existing loggers and any loggers created after this
    call.

    Args:
        level (int): The logging level to set (e.g., logging.DEBUG,
            logging.INFO).

    Examples:
        >>> from fxlog import fxlogger
        >>> fxlogger.set_loggers_level(fxlogger.DEBUG)
    """
    # Store as global default for future loggers
    global _DEFAULT_LEVEL
    _DEFAULT_LEVEL = level

    # First, update all explicitly tracked loggers
    for logger_name in _CONFIGURED_LOGGERS:
        logger_instance = logging.getLogger(logger_name)
        logger_instance.setLevel(level)
        for handler in logger_instance.handlers:
            handler.setLevel(level)

    # Then, also check formatters for any loggers we might have missed
    for logger_name in FXFormatter._loggers:
        if logger_name not in _CONFIGURED_LOGGERS:
            logger_instance = logging.getLogger(logger_name)
            logger_instance.setLevel(level)
            for handler in logger_instance.handlers:
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
