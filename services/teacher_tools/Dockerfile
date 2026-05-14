FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/service

RUN pip install --no-cache-dir uv

COPY pyproject.toml ./
COPY uv.lock ./
COPY src ./src

RUN uv sync --frozen --no-dev

EXPOSE 8010

CMD ["uv", "run", "uvicorn", "teacher_tools.api:app", "--host", "0.0.0.0", "--port", "8010"]
