FROM python:3.10-slim AS node

FROM node AS builder

RUN python3 -m venv /venv
ENV PATH=/venv/bin:$PATH

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

FROM node AS runner

COPY --from=builder /venv /venv
ENV PATH=/venv/bin:$PATH

COPY . .

RUN adduser --disabled-password --gecos "" appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]