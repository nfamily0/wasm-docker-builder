FROM ubuntu:latest

# ARG 정의: 기본값은 "default_value"
ARG BUILD_ARG="example"

RUN apt-get update && apt-get install -y \
    python3 git cmake xz-utils nodejs npm build-essential libeigen3-dev

RUN git clone https://github.com/emscripten-core/emsdk.git && \
    cd emsdk && \
    git pull && \
    ./emsdk install latest && \
    ./emsdk activate latest

RUN mkdir -p /usr/app/build