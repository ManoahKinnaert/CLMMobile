# add package dependencies
apk add git gcc python3 py3-pip zlib jpeg
# upgrade pip to latest version
python3 -m pip install --upgrade pip
# get setuptools and wheel
python3 -m pip install setuptools wheel
# install as a python package
python3 -m pip install git+https://github.com/ManoahKinnaert/CLMMobile.git