FROM python:3.11-slim

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY pyproject.toml uv.lock ./

RUN uv pip compile pyproject.toml -o requirements.txt && \
    uv pip install --system -r requirements.txt

COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

COPY . .

ENV PYTHONPATH=/app

EXPOSE 8082

ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8082"]