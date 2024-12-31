FROM python:3.12-slim-bookworm as base

FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM uv AS build

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    curl \
    && curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash \
    && apt-get install -y git-lfs \
    && git lfs install \
    && apt-get purge --auto-remove -y curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ADD .git /app/.git
ADD pyproject.toml uv.lock /app/

RUN git lfs pull && git submodule update --init --recursive --depth 1

RUN git submodule update --init --recursive

RUN uv sync --frozen

ADD . /app

FROM python:3.12-slim-bookworm AS runtime

WORKDIR /app

COPY --from=build /app /app
COPY --from=build /bin/uv /bin/uv

CMD ["uv", "run", "src/bot.py"]
