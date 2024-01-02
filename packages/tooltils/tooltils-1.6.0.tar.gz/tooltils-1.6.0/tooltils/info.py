"""General installation information"""


class _bm:
    from logging import (getLogger, Formatter, StreamHandler, DEBUG, 
                         INFO, WARN, ERROR, CRITICAL)
    from os import listdir, remove, mkdir
    from os.path import exists, abspath
    from time import localtime, mktime
    from datetime import datetime
    from json import load, dumps
    from shutil import rmtree
    from sys import platform
    from typing import Union

    from ._external import run

    class LoggingLevel:
        pass

    defaultData: dict = {
        "cache": {
            "errors": {},
            "global": {
                "configMethodValues": {}
            },
            "info": {},
            "main": {},
            "requests": {
                "verifiableTimesChecked": 0,
                "verifiableNetworkList": {},
                "connectedTimesChecked": 0,
                "connectedNetworkList": {}
            },
            "sys.info": {},
            "sys": {}
        },
        "config": {
            "errors": {},
            "global": {
                "config": {
                     "runConfigMethodAlways": False,
                     "configMethodCheck": 20
                } 
            },
            "info": {},
            "main": {},
            "requests": {
                "defaultVerificationMethod": True,
                "verifiableCachingCheck": 20,
                "connectedCachingCheck": 20,
                "verifiableCaching": False,
                "connectedCaching": False,
                "redirectLimit": 20
            },
            "sys.info": {},
            "sys": {}
        }
    }

    openData           = None
    actualConfig: dict = defaultData['config']
    split:         str = '\\' if platform.startswith('win') else '/'
    cdir:          str = split.join(__file__.split(split)[:3]) + split + '.tooltils' + split
    logger             = getLogger('tooltils.info')

    class levelFilter(object):
        def __init__(self, level):
            self.level = level

        def filter(self, logRecord):
            return logRecord.levelno <= self.level

    class lFormatter(Formatter):
        def formatTime(self, record, datefmt):
            return _bm.datetime.fromtimestamp(
                   _bm.mktime(_bm.localtime(record.created))).strftime(datefmt)


author:            str = str('feetbots')
"""The current owner of tooltils"""
author_email:      str = str('pheetbots@gmail.com')
"""The email of the current owner of tooltils"""
maintainer:        str = str('feetbots')
"""The current sustainer of tooltils"""
maintainer_email:  str = str('pheetbots@gmail.com')
"""The email of the current sustainer of tooltils"""
version:           str = str('1.6.0')
"""The current installation version"""
released:          str = str('1/1/2024')
"""The release date of the current version"""
description:       str = str('A lightweight python utility package built on the standard library')
"""The short description of tooltils"""
classifiers: list[str] = [
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.7",
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent"
]
"""The list of PyPi style tooltils classifiers"""
homepage:          str = str('https://github.com/feetbots/tooltils')
"""The current home website of tooltils"""
homepage_issues:   str = str('https://github.com/feetbots/tooltils/issues')
"""The current issues directory of the home website of tooltils"""
location:          str = str(_bm.split.join(__file__.split(_bm.split)[:-1]) + _bm.split)
"""The path of the current installation of tooltils"""
releases:    list[str] = ['1.0.0-beta', '1.1.0', '1.2.0', '1.3.0', '1.4.0', '1.4.1', '1.4.2',
                          '1.4.3', '1.4.4', '1.4.4-1', '1.5.0', '1.5.1', '1.5.2', '1.5.3',
                          '1.6.0']
"""All current versions of tooltils"""

license:   tuple[str] = (str('MIT License'), str("""
MIT License

Copyright (c) 2024 feetbots

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""))
"""The name and content of the currently used license in a tuple pair (name, content)"""
long_description: str = str("""
# tooltils | v1.6.0

[![python](https://img.shields.io/pypi/pyversions/tooltils.svg)](https://pypi.org/project/tooltils/)
[![downloads](https://static.pepy.tech/personalized-badge/tooltils?period=total&units=international_system&left_color=grey&right_color=red&left_text=downloads)](https://pepy.tech/project/tooltils)

A lightweight python utility package built on the standard library

```py
>>> import tooltils
>>> req = tooltils.requests.get('httpbin.org/get/')
>>> req
'<GET httpbin.org [200]>'
>>> req.url
'https://httpbin.org/get'
>>> req.status_code
'200 OK'
>>> req.headers["User-Agent"]
'Python-tooltils/1.6.0'
```

## Installation

Get the latest version from PyPi

```console
python -m pip install tooltils
```

OR build it directly from the source

```console
git clone https://github.com/feetbots/tooltils.git
cd tooltils
python -m pip install setup.py --user
```

## API

The full API is available to read in the project files at [**API.md**](API.md)

## Planned Features

- Add a different implementation of the `requests` module using some other library to include features like connection pooling
- (maybe) start including third party modules to add desireable features
- Stop using run of the mill implementations for everything

## Important Note

The current implementation for the cache and config, opens the data file once if used, then the code will use that specific TextIOWrapper class to write and read etc. Unfortunately, there is no native method of closing this file class once the program execution has ended, leaving this up to CPython's garbage collecter. This technique is bad practice but should be better than constantly opening and closing each file (performance reasons).
""")
"""The long description of tooltils"""

def _getData():
    if _bm.openData is None:
        _configMethods()

    return _bm.openData

def _loadCache(module: str='') -> dict:
    _f = _getData()
    data: dict = _bm.load(_f)['cache']
    _f.seek(0)

    if module == '':
        return data
    else:
        return data[module]

def _editCache(module: str, option: dict, subclass: str='') -> None:
    _f = _getData()
    data = _bm.load(_f)

    if subclass:
        data['cache'][module][subclass].update(option)
    else:
        data['cache'][module].update(option)

    _f.seek(0)
    _f.truncate()
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

def _deleteCacheKey(module: str, key: str, subclass: str='') -> None:
    _f = _getData()
    data = _bm.load(_f)

    if subclass:
        keys = data['cache'][module][subclass].keys()
    else:
        keys = data['cache'][module].keys()

    for i in list(keys):
        if key == i:
            if subclass:
                data['cache'][module][subclass].pop(i)
            else:
                data['cache'][module].pop(i)

    _f.seek(0)
    _f.truncate()
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

def _loadConfig(module: str='') -> dict:
    if module == '':
        return _bm.actualConfig
    else:
        return _bm.actualConfig[module]

#def _editConfig(module: str, option: dict, subclass: str='') -> None:
#    _f = _getData()
#    data: dict = _bm.load(_f)
#
#    if subclass:
#        data['config'][module][subclass].update(option)
#    else:
#        data['config'][module].update(option)
#
#    _f.seek(0)
#    _f.truncate()
#    _f.write(_bm.dumps(data, indent=4))
#    _f.seek(0)

def clearCache(module: str=None) -> None:
    """Clear the file cache of tooltils or a specific module within"""

    module: str = str(module).lower()
    _f          = _getData()
    wdata: dict = _bm.load(_f)

    if module == 'none':
        data: dict = _bm.defaultData['cache']
    else:
        data: dict = wdata['cache']

        try:
            data.update(_bm.defaultData['cache'][module])
        except KeyError:
            raise FileNotFoundError('Cache module not found')
        
    wdata['cache'] = data

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(wdata, indent=4))
    _f.seek(0)

    _bm.logger.debug('User cache was cleared')

def clearConfig(module: str=None) -> None:
    """Revert the config of tooltils or a specific module within"""

    module: str = str(module).lower()
    _f          = _getData()
    wdata: dict = _bm.load(_f)

    if module == 'none':
        data: dict = _bm.defaultData['config']
    else:
        data: dict = wdata['config']

        try:
            data.update(_bm.defaultData['config'][module])
        except KeyError:
            raise FileNotFoundError('Config module not found')
        
    wdata['config'] = data

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(wdata, indent=4))
    _f.seek(0)

    _bm.logger.debug('User config was reset')

def clearData() -> None:
    """Clear the cache and config of tooltils"""

    _f         = _getData()
    data: dict = _bm.load(_f)
    data.update(_bm.defaultData)

    _f.seek(0)
    _f.truncate(0)
    _f.write(_bm.dumps(data, indent=4))
    _f.seek(0)

    _bm.logger.debug('User cache and config was cleared and reset')

def deleteData(version: str=None) -> None:
    """Delete the data file for a specific tooltils version or all present"""

    if version is None:
        if not _bm.exists(_bm.cdir):
            raise FileNotFoundError('The tooltils storage directory does not exist')
        else:
            _bm.rmtree(_bm.cdir)

            _bm.logger.debug('User storage directory was deleted')
    else:
        if type(version) is not str:
            raise TypeError('Version must be a valid \'str\' instance')
        if version[0] == 'v':
            version: str = version[1:]
        if version not in releases:
            raise ValueError('Version not found in valid releases')

        try:
            _bm.remove(_bm.cdir + 'data-v' + version + '.json')

            _bm.logger.debug(f'User storage data file version v{version} was deleted')
        except FileNotFoundError:
            raise FileNotFoundError('Version data file not found in tooltils directory')

class logger():
    """Create a logging instance for tooltils modules only"""

    def enable(self) -> None:
        """Enable the logger instance"""

        if self._closed:
            raise ValueError('The logger has already been closed')
        elif self._enabled:
            raise ValueError('The logger is already enabled')
        else:
            self._enabled:   bool = True
            self._logger.disabled = False

    def disable(self) -> None:
        """Disable the logger instance"""

        if self._closed:
            raise ValueError('The logger has already been closed')
        elif not self._enabled:
            raise ValueError('The logger is already disabled')
        else:
            self._enabled:   bool = False
            self._logger.disabled = True
    
    def close(self) -> None:
        """Close the logger instance"""

        if self._closed:
            raise ValueError('The logger has already been closed')
        else:
            self._closed:   bool = True
            self._enabled:  bool = False
            self._logger.disabled = True
            self._logger.close()

    @property
    def module(self) -> str:
        """What module the logging is enabled for"""

        return self._module
    
    @module.setter
    def module(self, value):
        raise AttributeError('Module property cannot be changed')

    @property
    def level(self) -> _bm.Union[str, int, _bm.LoggingLevel]:
        """What level of logging is being used"""

        return self._level
    
    @level.setter
    def level(self, value):
        raise AttributeError('Level property cannot be changed')
    
    @property
    def level2(self) -> _bm.Union[str, int, _bm.LoggingLevel]:
        """What max level of logging is being used"""

        return self._level2
    
    @level2.setter
    def level2(self, value):
        raise AttributeError('Level2 property cannot be changed')

    @property
    def enabled(self) -> bool:
        """Whether the logger is enabled"""

        return self._enabled
    
    @enabled.setter
    def enabled(self, value):
        raise AttributeError('Enabled property cannot be changed')

    @property
    def closed(self) -> bool:
        """Whether the logger has been closed"""

        return self._closed
    
    @closed.setter
    def closed(self, value):
        raise AttributeError('Closed property cannot be changed')
    
    def enable(self) -> None:
        """Enable the logger instance"""

        self._enabled = not _bm.enable(self._logger, self.enabled, self.closed)
    
    def disable(self) -> None:
        """Disable the logger instance"""

        self._enabled = bool(_bm.disable(self._logger, self.enabled, self.closed))
    
    def close(self) -> None:
        """Close the logger instance"""
        
        self._disabled = True
        self._closed   = not _bm.close(self._logger, self.closed)

    def __init__(self, 
                 module: str='ALL', 
                 level: _bm.Union[str, int, _bm.LoggingLevel]='ALL',
                 level2: _bm.Union[str, int, _bm.LoggingLevel]='ALL'
                 ) -> None:
        if type(level) is str: level = level.upper()
        if type(level2) is str: level2 = level2.upper()
        
        if type(module) is not str:
            raise TypeError('Module must be a valid \'str\' instance')
        elif module.upper() not in ('', 'ALL', 'MAIN', 'REQUESTS', 'SYS'):
            raise ValueError('Unknown module \'{}\''.format(module))
        else:
            self._module: str = module.upper()

            if module == '' or module == 'ALL' or module == 'MAIN':
                self._module: str = 'tooltils'
            else:
                self._module: str = 'tooltils.' + module.lower()

        for i in (('level', level), ('level2', level2)):
            if not isinstance(i[1], (str, int, _bm.DEBUG, _bm.INFO, _bm.WARN,
                                     _bm.ERROR, _bm.CRITICAL)):
                raise TypeError(f'{i[0]} must be a valid \'str\', \'int\' or \'logging\' level instance')
            elif i[1] not in ('ALL', 'DEBUG', 'INFO', 'WARN', 'ERROR', 'CRITICAL', 10, 20, 30, 40, 50):
                raise ValueError('Invalid level \'{}\''.format(i[1]))
            else:
                if i[0] == 'level':
                    if level == 'ALL':
                        self._level = _bm.DEBUG
                    else:
                        self._level = level
                else:
                    if level2 == 'ALL':
                        self._level2 = _bm.CRITICAL
                    else:
                        self._level2 = level2
        
        self.logger = _bm.getLogger(self._module)
        handler     = _bm.StreamHandler()
        handler.      setFormatter(_bm.lFormatter(
                      '[%(asctime)s] [%(name)s/%(levelname)s]: %(message)s', '%H:%M:%S'))

        self.logger.setLevel(self._level)
        self.logger.addFilter(_bm.levelFilter(self._level2))
        self.logger.addHandler(handler)

        self._closed  = False
        self._enabled = True

        for k, v in {10: "DEBUG", 20: "INFO", 30: "WARN", 40: "ERROR", 50: "CRITICAL"}.items():
            if self._level == k:
                r1 = v
            elif self._level2 == k:
                r2 = v
        
        _bm.logger.debug(f'Initiated logger for <{self._module}> with range {r1} -> {r2}')

    def __str__(self) -> str:
        module: str = 'ALL' if not self.module else self.module.upper()
        state:  str = 'on' if self.enabled else 'off'

        return f'<Logger instance: [{state}] -> [{module}]>'

def _getFiles(dir: str) -> list:
    fileList: list = []

    for i in _bm.listdir(location + dir):
        fileList.append(location + ('' if not dir else dir + _bm.split) + i)
        
    return fileList

def _getLines():
    lines:  int = 0
    files: list = _getFiles('') + _getFiles('requests') + _getFiles('sys')

    for i in ('README.md', 'API.md', 'CHANGELOG.md', 'test.py', 'LICENSE', '.DS_Store',
            '__pycache__', '.git'):
        try:
            files.remove(location + i)
        except ValueError:
            continue

    for i in files:
        try:
            with open(i) as _f:
                lines += len(_f.readlines())
        except (IsADirectoryError, UnicodeDecodeError, PermissionError):
            pass
    
    _bm.logger.debug(f'Reported {lines} lines across {len(files)} items')
    
    return lines

lines: int = int(_getLines())
"""The amount of lines of code in this tooltils installation"""

def _configMethods():
    _f           = open(location + 'data.json', 'r+')
    _bm.openData = _f
    data: dict   = _bm.load(_f)
    _f.            seek(0)
    funcs: dict  = data['cache']['global']['configMethodValues']

    for k, v in data['config'].items():
        for k2, v2 in v.items():
            if type(v2) is str and '$f' in v2:
                try:
                    statement: str = v2.split(' ')[1].split('(')
                    funcName:  str = statement[0]
                    args:      str = '[' + statement[1][:-1] + ']'

                    if funcName in tuple(funcs.keys()) and funcs[funcName][1] < data[
                       'config']['global']['config']['configMethodCheck']:
                        funcs[funcName] = (funcs[funcName][0], funcs[funcName][1] + 1)
                        _editCache('global', {"configMethodValues": funcs})
                    else:
                        value = _bm.run(funcName, args)

                        funcs.update({funcName: (value, 1)})
                        _editCache('global', {"configMethodValues": funcs})
                except:
                    value = None
            else:
                value = v2

            _bm.actualConfig[k][k2] = value

    return _f

if not _bm.exists(_bm.cdir):
    _bm.mkdir(_bm.cdir)
    _bm.logger.debug('User storage directory does not exist, creating one now...')

    _create: bool = True
elif not _bm.exists(_bm.cdir + 'data-v' + version + '.json'):
    _create: bool = True
else:
    _create: bool = False

if _create:
    _bm.logger.debug('Current tooltils version data file does not exist, creating one now...')

    with open(_bm.cdir + 'data-v' + version + '.json', 'a+') as _f:
        _f.write(_bm.dumps(_bm.defaultData, indent=4))

del _getFiles, _getLines, _create
