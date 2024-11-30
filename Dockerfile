# Usa la imagen base de Python
FROM python:3.10.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    netcat-openbsd \
    postgresql-client

COPY pyproject.toml /app/

RUN pip install poetry

RUN poetry config virtualenvs.create false

RUN poetry install

COPY app/ /app/

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
EXPOSE 8001

ENTRYPOINT ["/entrypoint.sh"]