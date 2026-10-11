# CLMMobile

[![tests](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml/badge.svg)](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml)

## Basic installation on ISH (for ios and ipados)
To install (this can take a while):
```bash
apk add curl && curl -fsSL https://raw.githubusercontent.com/ManoahKinnaert/CLMMobile/main/install_ish.sh | ash
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