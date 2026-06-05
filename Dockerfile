FROM python:3.12-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN addgroup --system --gid 1000 appuser && \
    adduser --system --uid 1000 --ingroup appuser appuser

WORKDIR /app
COPY --chown=appuser:appuser app.py .

COPY pyproject.toml uv.lock ./

RUN uv sync --locked --no-cache --no-install-project

COPY app/ ./app/

ENV PATH="/app/.venv/bin:$PATH" \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app

USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0","--port", "8000"]