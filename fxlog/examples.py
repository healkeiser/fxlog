"""Example script for using fxlogger.

This module demonstrates various features of the fxlogger module:
    - Basic logging with color and separators
    - Custom message colors per log call
    - Multiple loggers
    - Saving logs to files
    - Changing log levels globally
    - Log file management (delete old logs, clear logs)

Examples:
    Run with default settings (color and separator enabled):
        >>> python examples.py

    Run with all features disabled:
        >>> python examples.py --no-color --no-separator

    Run with file logging enabled:
        >>> python examples.py --save-to-file --log-dir ./logs

    Show all available examples:
        >>> python examples.py --help
"""

import argparse
import tempfile
from pathlib import Path

from fxlog import fxlogger


def example_basic_logging(
    enable_color: bool = True, enable_separator: bool = True
) -> None:
    """Demonstrate basic logging with different log levels.

    Args:
        enable_color: Whether to enable color in log output.
        enable_separator: Whether to enable a separator in log output.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Basic Logging")
    print("=" * 60)

    logger = fxlogger.configure_logger(
        logger_name="basic_example",
        enable_color=enable_color,
        enable_separator=enable_separator,
        save_to_file=False,
    )
    logger.setLevel(fxlogger.DEBUG)

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


def example_custom_colors() -> None:
    """Demonstrate custom message colors per log call.

    The fxlogger module allows you to specify a custom color for each
    log message, overriding the default level-based colors.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Custom Message Colors")
    print("=" * 60)

    logger = fxlogger.configure_logger(
        logger_name="color_example",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )
    logger.setLevel(fxlogger.DEBUG)

    # Use custom colors for specific messages
    logger.info("Default green info message")
    logger.info("This info message is blue!", color=fxlogger.BLUE)
    logger.info("This info message is red!", color=fxlogger.RED)
    logger.info("This info message is magenta!", color=fxlogger.MAGENTA)

    # Combine colors with styles
    logger.debug(
        "Bright cyan debug message", color=fxlogger.CYAN + fxlogger.BRIGHT
    )
    logger.warning("Dim yellow warning", color=fxlogger.YELLOW + fxlogger.DIM)

    # Custom colors work with all log levels
    logger.error(
        "Error in blue for visibility", color=fxlogger.BLUE + fxlogger.BRIGHT
    )


def example_multiple_loggers() -> None:
    """Demonstrate using multiple loggers simultaneously.

    Each module in your application can have its own logger with a
    unique name, making it easy to track where log messages originate.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Multiple Loggers")
    print("=" * 60)

    # Create loggers for different "modules"
    db_logger = fxlogger.configure_logger(
        logger_name="database",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )
    api_logger = fxlogger.configure_logger(
        logger_name="api.handler",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )
    auth_logger = fxlogger.configure_logger(
        logger_name="auth.service",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )

    # Set levels
    db_logger.setLevel(fxlogger.DEBUG)
    api_logger.setLevel(fxlogger.INFO)
    auth_logger.setLevel(fxlogger.WARNING)

    # Simulate application activity
    db_logger.debug("Connecting to database...")
    db_logger.info("Database connection established")
    api_logger.info("API server starting on port 8080")
    api_logger.debug("This won't show - level is INFO")
    auth_logger.warning("Authentication token expires in 5 minutes")
    auth_logger.error("Failed login attempt from 192.168.1.100")


def example_global_level_change() -> None:
    """Demonstrate changing log levels globally for all loggers.

    The set_loggers_level() function allows you to change the log level
    for all configured loggers at once.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Global Level Change")
    print("=" * 60)

    logger1 = fxlogger.configure_logger(
        logger_name="service_a",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )
    logger2 = fxlogger.configure_logger(
        logger_name="service_b",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )

    # Initially set to DEBUG
    logger1.setLevel(fxlogger.DEBUG)
    logger2.setLevel(fxlogger.DEBUG)

    print("\n--- All loggers at DEBUG level ---")
    logger1.debug("Service A debug message")
    logger2.debug("Service B debug message")

    # Change all loggers to WARNING level globally
    print("\n--- Changing all loggers to WARNING level ---")
    fxlogger.set_loggers_level(fxlogger.WARNING)

    logger1.debug("This debug won't show")
    logger1.info("This info won't show")
    logger1.warning("Service A warning - this shows!")
    logger2.warning("Service B warning - this shows!")


def example_file_logging(log_dir: Path) -> None:
    """Demonstrate saving logs to files.

    Args:
        log_dir: Directory where log files will be saved.

    Note:
        Log files are organized by: {computer_name}/{username}/{date}.log
        All loggers share the same file handler for efficiency.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: File Logging")
    print("=" * 60)

    # Set the log directory first
    fxlogger.set_log_directory(log_dir)
    print(f"Log directory set to: {log_dir}")

    logger = fxlogger.configure_logger(
        logger_name="file_example",
        enable_color=True,
        enable_separator=True,
        save_to_file=True,
    )
    logger.setLevel(fxlogger.DEBUG)

    logger.info("This message is saved to both console and file")
    logger.warning("Warnings are also saved")
    logger.error("Errors too!")

    print(f"\nLog files created in: {log_dir}")
    # List created log files
    for item in log_dir.rglob("*.log"):
        print(f"  - {item.relative_to(log_dir)}")


def example_graceful_fallback() -> None:
    """Demonstrate graceful fallback when log directory is not set.

    If save_to_file=True but the log directory is not configured,
    fxlogger will print a warning and continue with console-only logging.
    """
    print("\n" + "=" * 60)
    print("EXAMPLE: Graceful Fallback (no log directory)")
    print("=" * 60)

    # Note: We're not calling set_log_directory() here
    # The logger will warn but continue working
    logger = fxlogger.configure_logger(
        logger_name="fallback_example",
        enable_color=True,
        enable_separator=False,
        save_to_file=True,  # This will trigger the warning
    )
    logger.setLevel(fxlogger.INFO)

    logger.info("Logger works fine even without file logging configured")


def example_available_colors() -> None:
    """Display all available colors and styles."""
    print("\n" + "=" * 60)
    print("EXAMPLE: Available Colors and Styles")
    print("=" * 60)

    logger = fxlogger.configure_logger(
        logger_name="colors_demo",
        enable_color=True,
        enable_separator=False,
        save_to_file=False,
    )
    logger.setLevel(fxlogger.INFO)

    colors = [
        ("BLACK", fxlogger.BLACK),
        ("BLUE", fxlogger.BLUE),
        ("CYAN", fxlogger.CYAN),
        ("GREEN", fxlogger.GREEN),
        ("MAGENTA", fxlogger.MAGENTA),
        ("RED", fxlogger.RED),
        ("WHITE", fxlogger.WHITE),
        ("YELLOW", fxlogger.YELLOW),
    ]

    print("\nColors:")
    for name, color in colors:
        logger.info(f"This is {name}", color=color)

    print("\nStyles:")
    logger.info("BRIGHT style", color=fxlogger.GREEN + fxlogger.BRIGHT)
    logger.info("DIM style", color=fxlogger.GREEN + fxlogger.DIM)
    logger.info("Normal style", color=fxlogger.GREEN)


def main() -> None:
    """Run all examples based on command line arguments."""
    parser = argparse.ArgumentParser(
        description="Example script demonstrating fxlogger features.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python examples.py                     Run with defaults (color + separator)
  python examples.py --no-color          Disable colors
  python examples.py --all               Run all examples
  python examples.py --save-to-file      Enable file logging (uses temp dir)
  python examples.py --log-dir ./logs    Specify custom log directory
        """,
    )
    parser.add_argument(
        "--no-color",
        action="store_true",
        help="Disable color in log output",
    )
    parser.add_argument(
        "--no-separator",
        action="store_true",
        help="Disable separator in log output",
    )
    parser.add_argument(
        "--save-to-file",
        action="store_true",
        help="Enable saving logs to files",
    )
    parser.add_argument(
        "--log-dir",
        type=Path,
        default=None,
        help="Directory for log files (default: system temp directory)",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all examples",
    )
    parser.add_argument(
        "--example",
        choices=[
            "basic",
            "colors",
            "multiple",
            "global-level",
            "file",
            "fallback",
            "available-colors",
        ],
        help="Run a specific example",
    )

    args = parser.parse_args()

    enable_color = not args.no_color
    enable_separator = not args.no_separator

    if args.example:
        # Run specific example
        if args.example == "basic":
            example_basic_logging(enable_color, enable_separator)
        elif args.example == "colors":
            example_custom_colors()
        elif args.example == "multiple":
            example_multiple_loggers()
        elif args.example == "global-level":
            example_global_level_change()
        elif args.example == "file":
            log_dir = args.log_dir or Path(tempfile.mkdtemp(prefix="fxlog_"))
            log_dir.mkdir(parents=True, exist_ok=True)
            example_file_logging(log_dir)
        elif args.example == "fallback":
            example_graceful_fallback()
        elif args.example == "available-colors":
            example_available_colors()
    elif args.all:
        # Run all examples
        example_basic_logging(enable_color, enable_separator)
        example_custom_colors()
        example_multiple_loggers()
        example_global_level_change()
        example_available_colors()

        if args.save_to_file:
            log_dir = args.log_dir or Path(tempfile.mkdtemp(prefix="fxlog_"))
            log_dir.mkdir(parents=True, exist_ok=True)
            example_file_logging(log_dir)
        else:
            example_graceful_fallback()
    else:
        # Default: run basic example
        example_basic_logging(enable_color, enable_separator)

        if args.save_to_file:
            log_dir = args.log_dir or Path(tempfile.mkdtemp(prefix="fxlog_"))
            log_dir.mkdir(parents=True, exist_ok=True)
            example_file_logging(log_dir)


if __name__ == "__main__":
    main()
