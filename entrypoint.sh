#!/bin/bash
set -e

cd /app/backend

# Run migrations
python manage.py migrate --noinput

# Seed data if DB is fresh (no vocabulary items)
python -c "
import django; django.setup()
from vocabulary.models import VocabularyItem
if VocabularyItem.objects.count() == 0:
    print('Fresh DB detected, seeding...')
    import subprocess
    subprocess.run(['python', 'manage.py', 'seed_content'], check=True)
    subprocess.run(['python', 'manage.py', 'seed_lessons'], check=True)
    print('Seeding complete')
else:
    print(f'DB has {VocabularyItem.objects.count()} vocab items, skipping seed')
"

# Collect static files
python manage.py collectstatic --noinput 2>/dev/null || true

# Start server
exec waitress-serve --port=8001 --url-scheme=https deutschmachine.wsgi:application
