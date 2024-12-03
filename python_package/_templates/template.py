"""Template module."""

# pylint: disable=unused-import, too-few-public-methods

# Built-in
import logging

# Third-party
import numpy as np

# Internal
from python_package import main


# Constants
PI = np.pi

# Logger
logger = logging.getLogger(__name__)


def hello_world() -> None:
    """Prints a greeting."""

    print("Hello, world!")


class HelloWorld:
    """A simple class with a single attribute."""

    def __init__(self):
        self.hello_world = "Hello, world!"

    def print(self) -> None:
        """Prints the attribute value."""

        print(self.hello_world)
