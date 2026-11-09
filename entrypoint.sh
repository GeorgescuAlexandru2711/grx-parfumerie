#!/bin/bash
set -e

echo "==> Running database migrations..."
python manage.py migrate --noinput

echo "==> Seeding database with initial fragrance catalogue (if empty)..."
python manage.py seed_catalog || true

exec "$@"
