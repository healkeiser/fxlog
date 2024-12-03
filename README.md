<div align="center">

  <h3 align="center">fxlog</h3>

  <p align="center">
    A custom logging module for Python that supports colorized output and log file rotation.
    <br/><br/>
    <!-- <a href="https://healkeiser.github.io/fxlog"><strong>Documentation</strong></a> -->
  </p>

  ##

  <p align="center">
    <!-- Maintenance status -->
    <img src="https://img.shields.io/badge/maintenance-actively--developed-brightgreen.svg?&label=Maintenance">&nbsp;&nbsp;
    <!-- <img src="https://img.shields.io/badge/maintenance-deprecated-red.svg?&label=Maintenance">&nbsp;&nbsp; -->
    <!-- License -->
    <img src="https://img.shields.io/badge/License-MIT-brightgreen.svg?&logo=open-source-initiative&logoColor=white" alt="License: MIT"/>&nbsp;&nbsp;
    <!-- PyPI -->
    <a href="https://pypi.org/project/fxlog">
      <img src="https://img.shields.io/pypi/v/fxlog?&logo=pypi&logoColor=white&label=PyPI" alt="PyPI version"/></a>&nbsp;&nbsp;
    <!-- PyPI downloads -->
    <a href="https://pepy.tech/project/fxlog">
      <img src="https://static.pepy.tech/badge/fxlog" alt="PyPI Downloads"></a>&nbsp;&nbsp;
    <!-- Last Commit -->
    <img src="https://img.shields.io/github/last-commit/healkeiser/fxlog?logo=github&label=Last%20Commit" alt="Last Commit"/>&nbsp;&nbsp;
    <!-- Commit Activity -->
    <a href="https://github.com/healkeiser/fxlog/pulse" alt="Activity">
      <img src="https://img.shields.io/github/commit-activity/m/healkeiser/fxlog?&logo=github&label=Commit%20Activity"/></a>&nbsp;&nbsp;
    <!-- GitHub stars -->
    <img src="https://img.shields.io/github/stars/healkeiser/fxlog" alt="GitHub Stars"/>&nbsp;&nbsp;
  </p>

</div>



<!-- TABLE OF CONTENTS -->
## Table of Contents

- [About](#about)
- [Installation](#installation)
- [How-to Use](#how-to-use)
  - [Save Log Files](#save-log-files)
  - [Do Not Save Log Files](#do-not-save-log-files)
  - [Set Log Level](#set-log-level)
  - [Set Formatter](#set-formatter)
- [Contact](#contact)



<!-- ABOUT -->
## About

A custom logging module for Python that supports colorized output and log file rotation. Includes features such as configurable log levels, custom formatters, and automatic deletion of old log files.



<!-- INSTALLATION -->
## Installation

The package can be installed via pip:

```bash
python -m pip install fxlog
```



<!-- HOW-TO USE -->
## How-to Use

You can use the `fxlog` module in your Python scripts as follows:

### Save Log Files

If you want to save the log files <sup>[1](#footnote1)</sup>, import the `fxlog` module, and set the log directory where log files will be stored:

```python
from fxlog import fxlogger

fxlog.set_log_directory('path/to/log/directory')
```

> [!NOTE]
> This only needs to be done once in your package.

Then, you can use the `fxlog` module to create a logger object and log messages to the console and a log file:

```python
from fxlog import fxlogger

logger = fxlog.configure_logger('my_logger')
logger.debug('This is a debug message')
```

To delete old log files, you can use the `fxlog` module as follows:

```python
from fxlog import fxlogger

fxlog.delete_old_logs(7) # Delete log files older than 7 days
```

You can also clear all log files in the log directory:

```python
from fxlog import fxlogger

fxlog.clear_logs()
```

> [!NOTE]
> <sup id="footnote1">1</sup> The log files are constructed with the following naming convention: `<logger_name>_<year>-<month>-<day>.log`.

### Do Not Save Log Files

If you don't want to save the log files, you can use the `fxlog` module as follows:

```python
from fxlog import fxlogger

logger = fxlog.configure_logger('my_logger', save_to_file=False)
logger.debug('This is a debug message')
```

### Set Log Level

You can set the log level of all loggers by using the `set_loggers_level` function:

```python
from fxlog import fxlogger

fxlog.set_loggers_level(fxlogger.DEBUG) # You can also use `logging.DEBUG`
```

### Set Formatter

By default, the output looks like this:

<p align="center">
  <img width="800" src="docs/images/basic.png">
</p>

You can enable a colored output by setting the `enable_color` parameter to `True`. The messages will be colorized according to their log levels:

```python
from fxlog import fxlogger

logger = fxlog.configure_logger('my_logger', enable_color=True)
logger.debug('This is a debug message')
```

<p align="center">
  <img width="800" src="docs/images/color.png">
</p>

> [!NOTE]
> Colors are not saved in log files.

> [!WARNING]
> If `enable_color` is set to `True` but the terminal does not support colorized output, the messages will be displayed in their original form.

You can also enable a separator between log messages by setting the `enable_separator` parameter to `True`:

```python
from fxlog import fxlogger

logger = fxlog.configure_logger('my_logger', enable_separator=True)
logger.debug('This is a debug message')
```

<p align="center">
  <img width="800" src="docs/images/color_separator.png">
</p>



<!-- CONTACT -->
## Contact

Project Link: [fxlog](https://github.com/healkeiser/fxlog)

<p align='center'>
  <!-- GitHub profile -->
  <a href="https://github.com/healkeiser">
    <img src="https://img.shields.io/badge/healkeiser-181717?logo=github&style=social" alt="GitHub"/></a>&nbsp;&nbsp;
  <!-- LinkedIn -->
  <a href="https://www.linkedin.com/in/valentin-beaumont">
    <img src="https://img.shields.io/badge/Valentin%20Beaumont-0A66C2?logo=linkedin&style=social" alt="LinkedIn"/></a>&nbsp;&nbsp;
  <!-- Behance -->
  <a href="https://www.behance.net/el1ven">
    <img src="https://img.shields.io/badge/el1ven-1769FF?logo=behance&style=social" alt="Behance"/></a>&nbsp;&nbsp;
  <!-- X -->
  <a href="https://twitter.com/valentinbeaumon">
    <img src="https://img.shields.io/badge/@valentinbeaumon-1DA1F2?logo=x&style=social" alt="Twitter"/></a>&nbsp;&nbsp;
  <!-- Instagram -->
  <a href="https://www.instagram.com/val.beaumontart">
    <img src="https://img.shields.io/badge/@val.beaumontart-E4405F?logo=instagram&style=social" alt="Instagram"/></a>&nbsp;&nbsp;
  <!-- Gumroad -->
  <a href="https://healkeiser.gumroad.com/subscribe">
    <img src="https://img.shields.io/badge/healkeiser-36a9ae?logo=gumroad&style=social" alt="Gumroad"/></a>&nbsp;&nbsp;
  <!-- Gmail -->
  <a href="mailto:valentin.onze@gmail.com">
    <img src="https://img.shields.io/badge/valentin.onze@gmail.com-D14836?logo=gmail&style=social" alt="Email"/></a>&nbsp;&nbsp;
  <!-- Buy me a coffee -->
  <a href="https://www.buymeacoffee.com/healkeiser">
    <img src="https://img.shields.io/badge/Buy Me A Coffee-FFDD00?&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee"/></a>&nbsp;&nbsp;
</p>