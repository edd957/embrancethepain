FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

COPY pyproject.toml README.md ./
COPY src ./src
COPY docs ./docs

RUN pip install --upgrade pip && pip install -e .

EXPOSE 8000

CMD ["uvicorn", "infrasentinel_ai.api.main:app", "--host", "0.0.0.0", "--port", "8000"]
