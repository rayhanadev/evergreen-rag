FROM python:3.12-slim-bookworm as base

FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM uv AS build

WORKDIR /app

RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

ADD .git /app/.git
ADD pyproject.toml /app/
ADD uv.lock /app/

RUN git submodule update --init --recursive

RUN uv sync --frozen

ADD . /app

FROM build AS runtime

CMD ["uv", "run", "src/bot.py"]
