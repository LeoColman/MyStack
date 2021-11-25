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


# Face Recognition
RUN apk add -X https://dl-cdn.alpinelinux.org/alpine/edge/testing dlib
RUN wget https://github.com/goodspb/pdlib/archive/master.zip \
  && mkdir -p /usr/src/php/ext/ \
  && unzip -d /usr/src/php/ext/ master.zip \
  && rm master.zip
RUN docker-php-ext-install pdlib-master
RUN apk add bzip2-dev
RUN docker-php-ext-install bz2