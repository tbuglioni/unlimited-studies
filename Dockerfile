FROM python:3.9-alpine3.14

ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/

# fix postegresl dependencies
RUN \
    apk add --no-cache postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    python3 -m pip install -r requirements.txt --no-cache-dir && \
    apk --purge del .build-deps

COPY . /code/


