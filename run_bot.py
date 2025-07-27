#!/usr/bin/env python3
import subprocess
import sys
import time

def install_requirements():
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "python-telegram-bot"])
        print("✅ Telegram bot library installed")
    except subprocess.CalledProcessError:
        print("❌ Failed to install telegram bot library")
        return False
    return True

def run_bot():
    if install_requirements():
        print("🚀 Starting Telegram bot...")
        try:
            subprocess.run([sys.executable, "telegram_bot.py"])
        except KeyboardInterrupt:
            print("\n🛑 Bot stopped")
        except Exception as e:
            print(f"❌ Bot error: {e}")

if __name__ == '__main__':
    run_bot()