FROM ubuntu:18.04

ENV PYTHONUNBUFFERED 1
ENV LC_ALL=C.UTF-8
ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install \
      build-essential \
      gcc \
      git \
      python3-venv \
      python3-dev \
      libmemcached-dev \
      libffi-dev \
      libpq-dev  \
      libssl-dev \
      gettext \
    && \
    apt-get clean && \
    mkdir /app && \
    useradd -m app

WORKDIR /app

ADD requirements.txt /app/

ENV PATH /home/app/venv/bin:${PATH}

RUN python3 -m venv ~/venv && \
    pip install --upgrade pip && \
    pip install wheel pip-tools && \
    pip-sync

ADD . /app/

ENV DJANGO_SETTINGS_MODULE app.settings

EXPOSE 8001

ENTRYPOINT [ "/app/manage.py" ]
