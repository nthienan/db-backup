FROM nthienan/python:3.6.6-alpine3.8-onbuild as builder

RUN python setup.py clean bdist_wheel

FROM alpine:3.10.0

ENV TZ=Africa/Abidjan

RUN apk --no-cache update && \
    apk --no-cache upgrade && \
    apk --no-cache add tzdata mariadb-client postgresql-client python3 git openssh && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --upgrade pip setuptools && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    if [ ! -e /usr/bin/python ]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
    rm -rf /var/cache/apk/* && \
    rm -rf /root/.cache

COPY ssh_config /root/.ssh/config
RUN chmod 400 /root/.ssh/config && \
    mkdir -p /var/db-backup/config
WORKDIR /var/db-backup
VOLUME /var/db-backup

COPY --from=builder /usr/src/app/dist/db_backup*.whl .
RUN pip install --no-cache-dir db_backup*.whl && \
    rm -f db_backup*.whl

ENTRYPOINT [ "db_backup.py" ]
CMD [ "-c", "/var/db-backup/config/db-backup.yaml" ]
