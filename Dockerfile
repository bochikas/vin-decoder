FROM python:3.11.4-alpine3.18

RUN apk update  \
    && apk add python3-dev \
                          gcc \
                          libc-dev \
                          libffi-dev

ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN pip install poetry

WORKDIR /usr/src

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY poetry.lock pyproject.toml ./

RUN poetry config virtualenvs.create false
RUN poetry install --no-interaction

COPY ./src ./