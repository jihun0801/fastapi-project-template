default:
    just --list

build:
    docker compose up -d --build

up:
    docker compose up -d

down *args:
    # -v: volume delete
    docker-compose down {{args}}

clean:
    docker-compose down -v --rmi all

kill:
    docker compose kill

ps:
    docker compose ps

exec *args:
    docker compose exec app {{args}}

# make migration
mm *args:
    docker compose exec app alembic revision --autogenerate -m "{{args}}"

migrate:
    docker compose exec app alembic upgrade head

downgrade *args:
    docker compose exec app alembic downgrade {{args}}

ruff *args:
    docker compose exec app ruff {{args}} src

black:
    docker compose exec app black src

lint:
    just black
    just ruff --fix

test:
    docker compose exec app pytest

reboot:
    just down -v
    just up
