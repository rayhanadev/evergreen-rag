FROM python:3.12-slim-bookworm as base

FROM base AS uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

FROM uv AS build

WORKDIR /app

ADD pyproject.toml /app/
ADD uv.lock /app/

RUN uv sync --frozen

ADD . /app

FROM build AS runtime

CMD ["uv", "run", "src/bot.py"]
