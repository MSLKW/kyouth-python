FROM python:3.14.4-bookworm

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /app

RUN mkdir src

COPY pyproject.toml uv.lock ./

COPY ./src/. ./src/.

RUN uv sync

ENTRYPOINT ["uv", "run", "uvicorn"]
CMD ["--app-dir", "src", "--host", "0.0.0.0", "--port", "8001", "main:app"]