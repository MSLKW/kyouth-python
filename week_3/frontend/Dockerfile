FROM python:3.14.4-bookworm

COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/

WORKDIR /var/www/frontend

RUN mkdir src

COPY pyproject.toml uv.lock ./

COPY ./src/main.py ./src/main.py
COPY ./src/templates/. ./src/templates/.

RUN uv sync

ENTRYPOINT ["uv", "run", "uvicorn"]
CMD ["--app-dir", "src", "--host", "0.0.0.0", "main:app"]