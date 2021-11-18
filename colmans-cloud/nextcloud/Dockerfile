FROM nextcloud:fpm-alpine

# For compiling and building
RUN apk add --update alpine-sdk

# Installing Python because some apps need it
RUN apk add py3-setuptools
RUN apk add py3-pip
RUN python3 -m pip install --upgrade pip
RUN apk add python3-dev jpeg-dev zlib-dev libjpeg
# Required Modules
RUN python3 -m pip install wheel
RUN python3 -m pip install --upgrade Pillow
RUN python3 -m pip install --upgrade numpy
# FFMPEG
RUN apk add ffmpeg
