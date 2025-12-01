# 🚀 Deploying Telegram News Bot to a VPS

This guide will help you deploy your bot to a Virtual Private Server (VPS) so it runs 24/7 reliably.

## Prerequisites
- A VPS (e.g., DigitalOcean, Vultr, Hetzner, AWS EC2) running **Ubuntu 20.04/22.04** or Debian.
- SSH access to your server.
- Your `.env` file credentials (API keys, etc.).

---

## Step 1: Connect to Your VPS
Open your terminal and SSH into your server:
```bash
ssh root@your_server_ip
```

## Step 2: Copy Files to VPS
You can use `scp` (secure copy) to upload your project files to the server. Run this **from your local machine**:

```bash
# Replace with your actual server IP and path
scp -r /path/to/telegram-news-bot root@your_server_ip:/root/
```

*Alternatively, you can git clone the repo on the server if you have it hosted.*

## Step 3: Run the Deployment Script
Back in your **VPS terminal**, navigate to the folder and run the script:

```bash
cd telegram-news-bot
chmod +x deploy.sh
./deploy.sh
```

**That's it!** The script will:
1. Install all system dependencies.
2. Set up the Python environment.
3. Install required libraries.
4. Create and start the background service.

## Step 4: Configure .env (If missing)
If you didn't copy your `.env` file, create it now:
```bash
nano .env
```
Paste your API keys and save (`Ctrl+O`, `Enter`, `Ctrl+X`). Then restart the bot:
```bash
systemctl restart telegram-bot
```

## 🛠 Managing the Bot

### Check Status
```bash
systemctl status telegram-bot
```

### View Live Logs
```bash
journalctl -u telegram-bot -f
```

### Stop/Start/Restart
```bash
systemctl stop telegram-bot
systemctl start telegram-bot
systemctl restart telegram-bot
```
