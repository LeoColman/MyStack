FROM lchaia/alpine-gcc:7.4.0 as builder
RUN apk add libuv-dev openssl-dev libmicrohttpd git cmake

RUN apk add --repository https://dl-cdn.alpinelinux.org/alpine/edge/testing hwloc-dev

# Build XMRIG
ARG XMRIG_BUILD_ARGS="-DCMAKE_BUILD_TYPE=Release"
WORKDIR /xmrig
RUN git clone -b ${XMRIG_VERSION} --single-branch --depth 1 https://github.com/MoneroOcean/xmrig ./ && \
    sed -i 's/kMinimumDonateLevel = 1;/kMinimumDonateLevel = 0;/g' ./src/donate.h && \
    mkdir build && \
    cmake ${XMRIG_BUILD_ARGS} . && \
    make && \
    ./xmrig --help

FROM alpine
COPY --from=builder /xmrig/xmrig /bin/
RUN apk add libuv-dev
RUN apk add --repository https://dl-cdn.alpinelinux.org/alpine/edge/testing hwloc-dev
RUN adduser -S -D -H -h /xmrig miner
RUN xmrig --help
USER miner
ENTRYPOINT ["xmrig"]
CMD [ "--help" ]