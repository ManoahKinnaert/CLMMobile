# add package dependencies
apk add git gcc python3-dev py3-pip musl-dev zlib-dev jpeg-dev py3-gevent
# upgrade pip to latest version
python3 -m pip install --upgrade pip
# get setuptools and wheel
python3 -m pip install --upgrade setuptools wheel
# install as a python package
python3 -m pip install git+https://github.com/ManoahKinnaert/CLMMobile.git