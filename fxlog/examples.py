"""Example script for using fxlogger."""

import argparse
from fxlog import fxlogger

# Set the log directory (not needed for this example since we won't save logs to a file)
# fxlogger.set_log_directory("/path/to/log_directory")


def main(enable_color: bool = False, enable_separator: bool = False) -> None:
    """Main function for the example script.

    Args:
        enable_color: Whether to enable color in log output.
            Defaults to `False`.
        enable_separator: Whether to enable a separator in log output.
            Defaults to `False`.
    """

    # Configure the logger without saving logs to a file
    logger = fxlogger.configure_logger(
        logger_name="example_logger",
        enable_color=enable_color,
        enable_separator=enable_separator,
        save_to_file=False,
    )

    # Set the log level
    logger.setLevel(fxlogger.logging.DEBUG)

    # Log some messages
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Example script for using fxlogger."
    )
    parser.add_argument(
        "--enable-color",
        action="store_true",
        help="Enable color in log output (default: False)",
    )
    parser.add_argument(
        "--enable-separator",
        action="store_true",
        help="Enable separator in log output (default: False)",
    )
    args = parser.parse_args()
    main(
        enable_color=args.enable_color, enable_separator=args.enable_separator
    )
