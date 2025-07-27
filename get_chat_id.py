#!/usr/bin/env python3
import requests
from config.config import TELEGRAM_BOT_TOKEN

def get_chat_id():
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getUpdates"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            
            print("=" * 50)
            print("TELEGRAM CHAT ID FINDER")
            print("=" * 50)
            
            if data['result']:
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        print(f"Chat ID: {chat['id']}")
                        print(f"Chat Type: {chat['type']}")
                        if 'username' in chat:
                            print(f"Username: @{chat['username']}")
                        if 'title' in chat:
                            print(f"Title: {chat['title']}")
                        print("-" * 30)
            else:
                print("No messages found.")
                print("\nTo get your chat ID:")
                print("1. Open Telegram")
                print("2. Search for your bot: @YourBotName")
                print("3. Send any message to the bot")
                print("4. Run this script again")
                
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    get_chat_id()