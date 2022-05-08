FROM python:3.9.7

ARG ENVIRONMENT
ENV POETRY_VERSION=1.1

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /code

COPY ./poetry.lock /code/poetry.lock
COPY ./pyproject.toml /code/pyproject.toml
COPY ./db/ /code/db/

RUN poetry config virtualenvs.create false 
RUN poetry install $(test "$ENVIRONMENT" == production && echo "--no-dev") --no-interaction --no-ansi

COPY ./rest_api_sqlite/ /code/rest_api_sqlite/

CMD ["uvicorn", "rest_api_sqlite.service:app", "--host", "0.0.0.0", "--port", "80"]