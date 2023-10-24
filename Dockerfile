FROM python:3.10-slim as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-slim

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=requirements-stage /tmp/requirements.txt /code/

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./hr_system .

CMD ["bash", "entrypoint.sh"]
