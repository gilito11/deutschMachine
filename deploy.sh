#!/bin/bash
# Deploy script for deutschMachine on Contabo VPS
set -e

echo "=== deutschMachine Deploy ==="

# Build and start
docker compose -f docker-compose.prod.yml up -d --build

# Wait for DB
echo "Waiting for database..."
sleep 5

# Run migrations
docker exec deutschmachine-web python manage.py migrate --noinput

# Seed data (only first time)
if [ "$1" = "--seed" ]; then
    echo "Seeding vocabulary..."
    docker exec deutschmachine-web python manage.py seed_content
    echo "Seeding lessons..."
    docker exec deutschmachine-web python manage.py seed_lessons
fi

echo "=== Deploy complete ==="
echo "App running at https://learn.fincaradar.com"
docker compose -f docker-compose.prod.yml ps
