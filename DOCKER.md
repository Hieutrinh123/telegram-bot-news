# Docker Deployment Guide

This guide explains how to run the Telegram News Bot using Docker.

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (usually comes with Docker Desktop)
- `.env` file configured with your credentials

## Quick Start

### 1. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
nano .env  # Edit with your credentials
```

Required variables:
- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_API_ID`
- `TELEGRAM_API_HASH`
- `OPENROUTER_API_KEY`
- `TARGET_CHANNEL_ID`

### 2. Build and Run with Docker Compose

```bash
# Build and start the bot
docker-compose up -d

# View logs
docker-compose logs -f

# Stop the bot
docker-compose down
```

### 3. Health Check

Test if the bot is healthy:

```bash
# Run health check
docker-compose exec telegram-bot uv run python health_check.py

# Or use the built-in Docker health check
docker inspect --format='{{.State.Health.Status}}' telegram-bot-news
```

## Manual Docker Commands

### Build the Image

```bash
docker build -t telegram-bot-news .
```

### Run the Container

```bash
docker run -d \
  --name telegram-bot-news \
  --env-file .env \
  -v $(pwd)/sessions:/app/sessions \
  -v $(pwd)/news-source:/app/news-source \
  --restart unless-stopped \
  telegram-bot-news
```

### Run Immediately (Testing)

```bash
docker run --rm \
  --env-file .env \
  -v $(pwd)/sessions:/app/sessions \
  -v $(pwd)/news-source:/app/news-source \
  telegram-bot-news \
  uv run python main.py --now
```

## Common Operations

### View Logs

```bash
# Follow logs
docker-compose logs -f telegram-bot

# View last 100 lines
docker-compose logs --tail=100 telegram-bot

# View logs since 1 hour ago
docker logs --since 1h telegram-bot-news
```

### Restart the Bot

```bash
# Restart with docker-compose
docker-compose restart

# Or restart the container directly
docker restart telegram-bot-news
```

### Access Container Shell

```bash
# Using docker-compose
docker-compose exec telegram-bot /bin/bash

# Or directly
docker exec -it telegram-bot-news /bin/bash
```

### Run Commands Inside Container

```bash
# Test crawler
docker-compose exec telegram-bot uv run python crawler.py

# Test Twitter crawler
docker-compose exec telegram-bot uv run python twitter_crawler.py

# Run summary immediately
docker-compose exec telegram-bot uv run python main.py --now
```

## Volume Management

The bot uses two volumes for persistence:

### 1. Sessions Volume
```bash
-v $(pwd)/sessions:/app/sessions
```
Stores Telegram session files so you don't need to re-authenticate on every restart.

### 2. News Sources Volume
```bash
-v $(pwd)/news-source:/app/news-source
```
Mount the news-source directory so you can update channels without rebuilding.

## Troubleshooting

### Health Check Failing

```bash
# Run manual health check
docker-compose exec telegram-bot uv run python health_check.py

# Check container logs
docker-compose logs telegram-bot
```

### Session Authentication

On first run, Telethon needs authentication:

```bash
# Run interactively to enter phone/code
docker-compose run --rm telegram-bot uv run python crawler.py
```

### Update Channels

Edit `news-source/tele_channels.txt` or `news-source/twitter_channels.txt`:

```bash
nano news-source/tele_channels.txt
# No need to rebuild - just restart
docker-compose restart
```

### Rebuild After Code Changes

```bash
# Rebuild and restart
docker-compose up -d --build

# Force rebuild from scratch
docker-compose build --no-cache
docker-compose up -d
```

### Clean Up Everything

```bash
# Stop and remove containers
docker-compose down

# Remove volumes too
docker-compose down -v

# Remove images
docker rmi telegram-bot-news
```

## Production Deployment

### Deploy to a VPS

1. **Upload files to server**:
```bash
scp -r ./* user@your-server:/path/to/app/
```

2. **SSH into server**:
```bash
ssh user@your-server
cd /path/to/app/
```

3. **Configure and run**:
```bash
cp .env.example .env
nano .env  # Fill credentials
docker-compose up -d
```

### Auto-restart on Server Reboot

The `restart: unless-stopped` policy in `docker-compose.yml` ensures the bot restarts automatically.

To verify:
```bash
# Reboot server
sudo reboot

# After reboot, check status
docker ps
```

### Monitor Container

```bash
# Check container status
docker ps

# View resource usage
docker stats telegram-bot-news

# Check health status
docker inspect telegram-bot-news | grep -A 10 Health
```

## Environment Variables

All variables from `.env` are passed to the container:

```yaml
# docker-compose.yml includes:
env_file:
  - .env
```

You can also pass individual variables:

```bash
docker run -e TELEGRAM_BOT_TOKEN=xxx -e TELEGRAM_API_ID=123 ...
```

## Security Notes

- Never commit `.env` file to git
- Use Docker secrets for production deployments
- Keep session files secure (they grant access to your Telegram account)
- Regularly update the base image: `docker-compose pull && docker-compose up -d`

## Multi-platform Builds

Build for different architectures (useful for ARM servers like Raspberry Pi):

```bash
# Build for ARM64
docker buildx build --platform linux/arm64 -t telegram-bot-news:arm64 .

# Build for multiple platforms
docker buildx build --platform linux/amd64,linux/arm64 -t telegram-bot-news:latest .
```
