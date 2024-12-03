<div align="center">

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/Python_logo_and_wordmark.svg/2880px-Python_logo_and_wordmark.svg.png" alt="Logo" width="400">

  <h3 align="center">Python Package</h3>

  <p align="center">
    Template for Python packages.
    <br/><br/>
    <!-- <a href="https://healkeiser.github.io/python_package"><strong>Documentation</strong></a> -->
  </p>

  ##

  <p align="center">
    <!-- Maintenance status -->
    <img src="https://img.shields.io/badge/maintenance-actively--developed-brightgreen.svg?&label=Maintenance">&nbsp;&nbsp;
    <!-- <img src="https://img.shields.io/badge/maintenance-deprecated-red.svg?&label=Maintenance">&nbsp;&nbsp; -->
    <!-- License -->
    <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg?&logo=open-source-initiative&logoColor=white" alt="License: MIT"/>&nbsp;&nbsp;
    <!-- PyPI -->
    <!-- <a href="https://pypi.org/project/python_package">
      <img src="https://img.shields.io/pypi/v/python_package?&logo=pypi&logoColor=white&label=PyPI" alt="PyPI version"/></a>&nbsp;&nbsp; -->
    <!-- Last Commit -->
    <img src="https://img.shields.io/github/last-commit/healkeiser/python_package?logo=github&label=Last%20Commit" alt="Last Commit"/>&nbsp;&nbsp;
    <!-- Commit Activity -->
    <a href="https://github.com/healkeiser/python_package/pulse" alt="Activity">
      <img src="https://img.shields.io/github/commit-activity/m/healkeiser/python_package?&logo=github&label=Commit%20Activity"/></a>&nbsp;&nbsp;
    <!-- GitHub stars -->
    <img src="https://img.shields.io/github/stars/healkeiser/python_package" alt="GitHub Stars"/>&nbsp;&nbsp;
  </p>

</div>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [About](#about)
- [How-to Use](#how-to-use)
- [Auto Changelog](#auto-changelog)



<!-- ABOUT -->
## About

Python package template repository.



<!-- HOW-TO USE -->
## How-to Use

1. Use the repository as a template.
2. Clone the repository.
3. Build your package.



<!-- AUTO-CHANGELOG -->
## Auto Changelog

You can find the changelog [here](CHANGELOG.md). To run [`auto-changelog`](https://github.com/cookpete/auto-changelog), follow those [instructions](https://healkeiser.github.io/notes/development/javascript/auto-changelog/#install).

The commits containing the `README` or `CHANGELOG` characters will be ignored by `auto-changelog`. To include them, remove the following lines from the [`.auto-changelog`](.auto-changelog) file:

```json
{
    "ignoreCommitPattern": ".*(CHANGELOG|README).*",
}
```
