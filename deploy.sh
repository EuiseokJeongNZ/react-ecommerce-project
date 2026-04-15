#!/bin/bash
set -e

echo "==> Move to project"
cd /home/ubuntu/react-ecommerce-project

echo "==> Pull latest code"
git fetch origin
git reset --hard origin/main

echo "==> Move to server"
cd /home/ubuntu/react-ecommerce-project/server

echo "==> Stop old container"
docker rm -f purepro-backend-container || true

echo "==> Build image"
docker build -t purepro-backend .

echo "==> Run new container"
docker run -d \
  --name purepro-backend-container \
  --env-file .env.prod \
  -e DJANGO_SETTINGS_MODULE=config.settings.prod \
  -p 8000:8000 \
  --restart unless-stopped \
  purepro-backend

echo "==> Clean unused images"
docker image prune -f

echo "==> Done"