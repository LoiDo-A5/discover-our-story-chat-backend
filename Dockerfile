FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip
RUN pip install --upgrade poetry

WORKDIR /app

COPY pyproject.toml ./
COPY poetry.lock ./

RUN poetry install --no-root --only main