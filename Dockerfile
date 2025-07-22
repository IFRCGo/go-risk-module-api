FROM python:3.8-slim-bookworm AS base
COPY --from=ghcr.io/astral-sh/uv:0.7.4 /uv /uvx /bin/

LABEL maintainer="IFRC"
LABEL org.opencontainers.image.source="https://github.com/IFRCGo/go-risk-module-api"

ENV PYTHONUNBUFFERED=1

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_PROJECT_ENVIRONMENT="/usr/local/"

WORKDIR /code

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    apt-get update -y \
    && apt-get install -y --no-install-recommends \
        # Build required packages
        gdal-bin build-essential gcc g++ libc-dev libgdal-dev libproj-dev \
        # Helper packages
        git curl wait-for-it procps \
    && uv lock --locked --offline \
        && uv sync --frozen --no-install-project --all-groups \
    # Clean-up
    && apt-get remove -y build-essential gcc g++ libc-dev libgdal-dev libproj-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*


COPY . /code/
