FROM python:3.8-slim-buster

LABEL maintainer="Togglecorp Dev dev@togglecorp.com"

ENV PYTHONUNBUFFERED 1

WORKDIR /code

RUN apt-get -y update \
    && apt-get install -y --no-install-recommends \
        git \
        g++ \
        curl \
        gdal-bin \
        libgdal-dev


ARG CPLUS_INCLUDE_PATH=/usr/include/gdal
ARG C_INCLUDE_PATH=/usr/include/gdal
RUN pip install GDAL==2.4.0

COPY pyproject.toml poetry.lock /code/

# Upgrade pip and install python packages for code
RUN pip install --upgrade --no-cache-dir pip poetry \
    && poetry --version \
    # Configure to use system instead of virtualenvs
    && poetry config virtualenvs.create false \
    && poetry install --no-root \
    # Remove installer
    && pip uninstall -y poetry virtualenv-clone virtualenv


COPY . /code/
