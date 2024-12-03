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
install_requires = []

setup(
    name="python_package",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    description="Template for Python packages.",
    url="https://github.com/healkeiser/python_package",
    author="Valentin Beaumont",
    author_email="valentin.onze@gmail.com",
    license="MIT",
    keywords="",
    packages=find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    project_urls={
        "Documentation": "https://healkeiser.github.io/python_package",
        "GitHub": "https://github.com/healkeiser/python_package",
        "Changelog": "https://github.com/healkeiser/python_package/blob/main/CHANGELOG.md",
        "Source": "https://github.com/healkeiser/python_package",
        "Funding": "https://github.com/sponsors/healkeiser",
    },
)
