# CLMMobile

[![tests](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml/badge.svg)](https://github.com/ManoahKinnaert/CLMMobile/actions/workflows/testing.yml)

## Basic installation on ISH (for ios and ipados)
First you will need the ISH app on your iPhone or iPad.
You can find it [here](https://ish.app/).

Then copy the following and paste in ish and hit enter:
```bash
cat /dev/location > /dev/null &
```
This might ask you to enable location services in settings, please enable this. Enabling location services will allow to run CLMMobile in the background later.
You also might want to enable 'keep screen turned on' because the installation of some packages can take quite a while.

To install CLMMobile on ish(this can take a while):
```bash
apk add curl && curl -fsSL https://raw.githubusercontent.com/ManoahKinnaert/CLMMobile/main/install_ish.sh | ash
```

To launch:
```bash
python3 -m CLMMobile
```


## Installation from source
Clone the repo and navigate to folder:
```bash
git clone https://github.com/ManoahKinnaert/CLMMobile.git && cd CLMMobile
```

Create virtual environment (unix / linux):
```bash
python3 -m venv .venv && source .venv/bin/activate
```

Install:
```bash
pip install -e .
```

And of you go...

## Running tests
There is a testing suite (in progress), to run it do this:
```bash
python -m unittest discover -s tests -v
```