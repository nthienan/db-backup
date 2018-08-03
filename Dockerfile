FROM alpine:3.8

RUN apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add python3 && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -r /root/.cache

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . ./

ENTRYPOINT [ "/usr/src/app/entrypoint.py" ]
