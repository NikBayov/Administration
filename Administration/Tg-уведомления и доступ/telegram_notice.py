#!/usr/bin/env python3

import requests
import sys
import os

# Укажите ваш токен бота и список chat_id
TELEGRAM_BOT_TOKEN = "7374262153:AAFRq2V7OWVOSyMWJlJtMUTpdFQqFxnZ5bY"
CHAT_IDS = ["1955253408", "5084227190"] # Добавьте сюда нужные chat_id

# Получение информации о пользователе
def get_ssh_info():
    user = os.getenv('PAM_USER', 'Unknown')
    rhost = os.getenv('PAM_RHOST', 'Unknown')
    service = os.getenv('PAM_SERVICE', 'Unknown')
    tty = os.getenv('PAM_TTY', 'Unknown')
    
    return user, rhost, service, tty

# Функция отправки сообщения в Telegram
def send_telegram_message(chat_id, message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to chat_id {chat_id}: {e}")
        sys.exit(1)

# Основная логика выполнения
if __name__ == "__main__":
    user, rhost, service, tty = get_ssh_info()
    message = f"🔔 SSH Login Alert 🔔\nUser: {user}\nRemote Host: {rhost}\nService: {service}\nTTY: {tty}"
    
    for chat_id in CHAT_IDS:
        send_telegram_message(chat_id, message)
