FROM alpine as builder

LABEL maintainer="Sacha Korban"

RUN apk add --no-cache make gcc musl-dev git && \
	mkdir /build/ && cd /build/ && \
	git clone https://github.com/ebiggers/libdeflate.git && \
	cd libdeflate/ && make

FROM python:alpine

COPY entrypoint.py /entrypoint.py

COPY --from=builder /build/libdeflate/gzip /usr/local/bin/

RUN chmod +x /entrypoint.py && \
    apk add --no-cache brotli

ENTRYPOINT ["python3", "/entrypoint.py"]
