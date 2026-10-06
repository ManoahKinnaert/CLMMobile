# CLMMobile

[![tests](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml/badge.svg)](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml)

## Basic installation on ISH (for ios and ipados)
To install (this can take a while):
```bash
apk add python3 py3-pip && python3 -m pip install git+https://github.com/ManoahKinnaert/CLMMobile.git
```
To launch:
```bash
python3 -m CLMMobile
```

## Running tests
There is a testing suite (in progress), to run it do this:
```bash
python -m unittest discover -s tests -v
```