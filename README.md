# loggerpy

The simplest Python logger for everyday tasks.

[![](https://img.shields.io/github/v/release/mett96/loggerpy?color=orange)](https://github.com/mett96/loggerpy/releases/tag/v1.0)
[![](https://img.shields.io/pypi/v/loggerpy?color=green)](https://pypi.org/project/loggerpy/)
[![](https://img.shields.io/pypi/pyversions/loggerpy)](https://www.python.org/downloads/release/python-370/)
[![](https://img.shields.io/github/license/mett96/loggerpy)](https://github.com/mett96/loggerpy/blob/master/LICENSE.md)
<!-- [![](https://img.shields.io/github/stars/mett96/loggerpy?style=social)](https://github.com/mett96/loggerpy) -->



## Table of Contents

* [Installation](#Installation)
* [Instructions](#Instructions)
    * [Configuration](#Configuration)
    * [Logger](#Logger)
    * [Customization](#Customization)
    * [Logger Recovery](#LoggerRecovery)
* [Version](#Version)
* [Next release](#NextRelease)
* [License](#License)
<!-- * [Authors](#Authors) -->


## Installation

The easiest way to install is throw pip.

```bash
pip install loggerpy
```

Or you can install directly from Github
```bash
pip install git+https://github.com/mett96/loggerpy.git
```

## Instructions


In order to use this simple logger, many examples are provided inside [examples directory](https://github.com/mett96/loggerpy/tree/master/examples)

![logging ](https://raw.githubusercontent.com/mett96/loggerpy/master/imgs/logger_example.png)


### Configuration
The first thing to do is to configure the global settings of logger package.

```python
import loggerpy

loggerpy.configure()
```

The possible customization of configurations are:
- domain: the main name of all loggers
- path: the path of saving log if you want to save them
- print_level: the minimum level of printing 
- save_level: the minimum level of saving, they can be different
- info: boolean value if you want to print the default string _"Logger configured..."_

In order to simplify the customization of printing and saving level it is provided a class that contained the 6 possible levels of logging. 
Importing _Level_ from loggerpy, they can be used eg Level.DEBUG or Level.WARNING
- Level.NO_LOGGER
- Level.DEBUG
- Level.INFO
- Level.WARNING
- Level.ERROR
- Level.CRITICAL

Configuration [example](https://github.com/mett96/loggerpy/tree/master/examples/configuration.py)


### Logger
Now, it's time to create your first logger.
```python
from loggerpy import configure, get_logger

configure()

logger = get_logger('custom_name')

```

First logger [example](https://github.com/mett96/loggerpy/tree/master/examples/first_logger.py)

### Customization
When we use _get_logger_ we can set custom parameters for this specific logger.
They are independent from the parameters set during configuration.
The customizable parameters are:
- print_level
- save_level
- path

```python
logger = get_logger('first', print_level=Level.WARNING, save_level=Level.INFO, path='custom_logger')
```

The complete [example](https://github.com/mett96/loggerpy/tree/master/examples/custom_logger.py)

### LoggerRecovery
Each logger has a unique name. So, when you ask to _get_logger_ to create a logger with an already existing name, it returns an instance of the unique logger with input name.    
Only in this case, if it is given also a custom path it is ignored in order to not split the logs into different files

```python
logger = get_logger('unique_name')
logger1 = get_logger('unique_name')

print(logger1 == logger)
print(hash(logger))
print(hash(logger1))
```

The equality of the two loggers can be verified by printing the result of the equality of the two objects, or printing the hash of each object.

The complete the in the linkes [example](https://github.com/mett96/loggerpy/tree/master/examples/logger_recovery.py)


## Versions
*stable version*
- 1.0 : released

*development version*
- 1.1 : on going
    - [ ] introducing `pprint` and `json` to print better log
    - [ ] try to expose _Level methods without give the possibility to create a new object



## NextRelease
- [ ] custom _format_ for timestamp
- [ ] custom _format_ for all log
- [ ] custom _color_ for each level
- [ ] inherit the _domain_ from another logger

<!-- ## Authors -->

## License
This project is under the GPL-3.0 license - see the [LICENSE.md](LICENSE.md) file for more details
