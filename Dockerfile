FROM alpine:3.8

ENV TZ=Africa/Abidjan

RUN apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add tzdata mariadb-client python3 git && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY . ./
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "/usr/src/app/entrypoint.py" ]
