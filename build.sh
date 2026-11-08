#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR/frontend"
npm install
npm run build

cd "$ROOT_DIR/backend"
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate
