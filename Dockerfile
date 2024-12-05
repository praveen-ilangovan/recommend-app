# Based on: https://medium.com/@albertazzir/blazing-fast-python-docker-builds-with-poetry-a78a66f5aed0

FROM python:3.12.5-slim

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==1.8.3

WORKDIR /app

# Install app dependencies
COPY pyproject.toml poetry.lock ./
RUN touch README.md
RUN poetry install --without dev,docs --no-root && rm -rf $POETRY_CACHE_DIR

# Install the app
COPY recommend_app ./recommend_app
RUN poetry install --without dev,docs

# Add venv/bin to path, so python could be loaded from there
ENV VIRTUAL_ENV=./.venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

CMD ["poetry", "run", "app"]
