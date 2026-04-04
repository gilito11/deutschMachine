FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=deutschmachine.settings

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ backend/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app/backend

RUN python backend/manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8001

WORKDIR /app/backend

CMD ["/app/entrypoint.sh"]
