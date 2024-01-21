FROM python:3.10.0
ENV PYTHONPATH=/stealth_hw/app

LABEL author="baclrary"

WORKDIR /stealth_hw

COPY pyproject.toml poetry.lock* ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev  # no-dev to exclude development dependencies

COPY . .
