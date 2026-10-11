# add package dependencies
apk add gcc python3 zlib jpeg py3-flask py3-gevent py3-pillow
python3 -m ensurepip
# install as a python package
python3 -m pip install git+https://github.com/ManoahKinnaert/CLMMobile.git