FROM python:3.11.6 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes --with dev

FROM python:3.11.6

RUN apt-get update && \
    apt-get install -y gcc libpq-dev && \
    apt clean && \
    rm -rf /var/cache/apt/*

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8 \
    TZ=Asia/Seoul

COPY . /src
WORKDIR /src

COPY --from=requirements-stage /tmp/requirements.txt /src/requirements.txt

RUN pip install -U pip && \
    pip install --no-cache-dir -r /src/requirements.txt

ENV PATH "$PATH:/src/scripts"

RUN useradd -m -d /src -s /bin/bash app \
    && chown -R app:app /src/* && chmod +x /src/scripts/*

USER app

CMD ["./scripts/start-dev.sh"]