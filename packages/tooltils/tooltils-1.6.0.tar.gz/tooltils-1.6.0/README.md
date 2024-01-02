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
