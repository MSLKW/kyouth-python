FROM python:3.14.4-bookworm

RUN pip install fastapi \
				jinja2 \
				python-dotenv \
				uvicorn

WORKDIR /var/www/frontend

RUN mkdir src

COPY ./src/app.py ./src/main.py
COPY ./src/templates ./src/templates

ENTRYPOINT ["uv", "run" "uvicorn"]
CMD ["--app-dir", "src", "--host", "0.0.0.0", "main.app"]