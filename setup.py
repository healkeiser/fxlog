"""PyPI setup script."""

# Built-in
from pathlib import Path
from setuptools import setup, find_packages

# Metadata
__author__ = "Valentin Beaumont"
__email__ = "valentin.onze@gmail.com"


# Add `README.md` as project long description
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Required dependencies
install_requires = ["colorama"]

setup(
    name="fxlog",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="A custom logging module for Python that supports colorized "
    "output and log file rotation. Includes features such as configurable "
    "log levels, custom formatters, and automatic deletion of old log files.",
    url="https://github.com/healkeiser/fxlog",
    author="Valentin Beaumont",
    author_email="valentin.onze@gmail.com",
    license="MIT",
    keywords="",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    project_urls={
        "Documentation": "https://healkeiser.github.io/fxlog",
        "GitHub": "https://github.com/healkeiser/fxlog",
        "Changelog": "https://github.com/healkeiser/fxlog/blob/main/CHANGELOG.md",
        "Source": "https://github.com/healkeiser/fxlog",
        "Funding": "https://github.com/sponsors/healkeiser",
    },
)
