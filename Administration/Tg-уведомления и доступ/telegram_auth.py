import telegram
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import sys
import os
import asyncio
from datetime import datetime
import requests # Для получения информации о городе и провайдере
import subprocess # Для выполнения системных команд

# Конфигурация
TOKEN = '7374262153:AAFRq2V7OWVOSyMWJlJtMUTpdFQqFxnZ5bY' # Токен вашего Telegram-бота
CHAT_IDS = ['1955253408', '5084227190'] # Список ID чатов в Telegram, куда будут отправляться сообщения
IP_INFO_URL = 'http://ipinfo.io/{}/json' # URL для получения информации о IP-адресе (город, провайдер и т.д.)

# Создаем объект бота с использованием токена
bot = telegram.Bot(token=TOKEN)

# Словарь для хранения запросов на подтверждение
request_data = {}

def get_local_ip():
    """
    Функция для получения локального IP-адреса машины, на которой выполняется скрипт.
    Использует команду 'hostname -I' для получения IP-адресов и возвращает первый из них.
    """
    try:
        result = subprocess.run(['hostname', '-I'], capture_output=True, text=True)
        return result.stdout.strip().split()[0] # Возвращаем первый IP из списка
    except Exception:
        return 'Неизвестен' # Возвращаем 'Неизвестен' в случае ошибки

def get_hostname():
    """
    Функция для получения имени хоста машины, на которой выполняется скрипт.
    Использует команду 'hostname' для получения имени хоста.
    """
    try:
        result = subprocess.run(['hostname'], capture_output=True, text=True)
        return result.stdout.strip() # Возвращаем имя хоста
    except Exception:
        return 'Неизвестен' # Возвращаем 'Неизвестен' в случае ошибки

async def send_telegram_message(username, remote_ip, request_id):
    """
    Асинхронная функция для отправки сообщения в Telegram с информацией о попытке входа.
    Сообщение включает время входа, IP-адрес, информацию о городе и провайдере,
    локальный IP и имя хоста.
    """
    # Получаем информацию о IP
    ip_info = {}
    try:
        response = requests.get(IP_INFO_URL.format(remote_ip))
        ip_info = response.json() # Преобразуем ответ в формат JSON
    except Exception:
        ip_info = {} # Если возникла ошибка, оставляем словарь пустым

    # Извлекаем информацию из ответа
    city = ip_info.get('city', 'Неизвестно')
    provider = ip_info.get('org', 'Неизвестно')
    login_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # Текущее время в нужном формате
    local_ip = get_local_ip() # Получаем локальный IP
    hostname = get_hostname() # Получаем имя хоста

    # Формируем текст сообщения
    message = (f"🕒 Login Time: {login_time}\n"
             f"🏠 Hostname: {hostname}\n"
             f"📍 Remote IP: {remote_ip}\n"
             f"🌐 System IP: {local_ip}\n"
             f"🔌 Provider: {provider}\n"
             f"🏙️ City: {city}\n"
             f"👤 Username: {username}")
    
    # Создаем кнопки для ответа (разрешить или запретить вход)
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Разрешить", callback_data=f"allow_{request_id}"),
         InlineKeyboardButton("Запретить", callback_data=f"deny_{request_id}")]
    ])
    
    # Отправляем сообщение в каждый чат из списка CHAT_IDS
    for chat_id in CHAT_IDS:
        try:
            await bot.send_message(chat_id=chat_id, text=message, reply_markup=reply_markup)
        except Exception as e:
            print(f"Failed to send message to chat_id {chat_id}: {e}")

async def main():
    """
    Основная асинхронная функция, которая запускает процесс обработки входящих запросов.
    """
    global request_data
    username = os.getenv('PAM_USER') # Получаем имя пользователя из переменной окружения PAM_USER
    remote_ip = os.getenv('PAM_RHOST') # Получаем IP-адрес удаленного хоста из переменной окружения PAM_RHOST

    if not username or not remote_ip:
        sys.exit(1) # Если данные отсутствуют, завершаем выполнение с кодом 1

    # Создаем уникальный идентификатор запроса на основе текущего времени
    request_id = str(int(datetime.now().timestamp()))
    # Сохраняем информацию о запросе в словаре
    request_data[request_id] = {'username': username, 'remote_ip': remote_ip, 'timestamp': datetime.now().isoformat()}

    # Отправляем сообщение в Telegram с запросом на подтверждение входа
    await send_telegram_message(username, remote_ip, request_id)

    update_id = None # ID последнего обновления для бота
    start_time = datetime.now() # Время начала обработки запросов

    while True:
        try:
            # Проверяем, прошло ли более 60 секунд с начала обработки запросов
            if (datetime.now() - start_time).total_seconds() > 60:
                sys.exit(1) # Завершаем выполнение, если прошло больше 60 секунд

            # Получаем обновления от бота
            updates = await bot.get_updates(offset=update_id, timeout=10)
            for update in updates:
                update_id = update.update_id + 1 # Обновляем ID последнего обновления
                if update.callback_query: # Проверяем, есть ли обратный вызов с кнопки
                    callback_data = update.callback_query.data # Извлекаем данные из обратного вызова
                    if callback_data.startswith('allow_') or callback_data.startswith('deny_'):
                        req_id = callback_data.split('_')[1] # Извлекаем ID запроса из данных обратного вызова
                        if req_id in request_data:
                            if callback_data.startswith('allow_'):
                                del request_data[req_id] # Удаляем обработанный запрос из словаря
                                sys.exit(0) # Разрешаем вход
                            elif callback_data.startswith('deny_'):
                                del request_data[req_id] # Удаляем обработанный запрос из словаря
                                sys.exit(1) # Запрещаем вход
        except Exception:
            pass # Игнорируем ошибки в процессе обработки
        await asyncio.sleep(1) # Ожидаем перед следующим запросом

if __name__ == "__main__":
    asyncio.run(main()) # Запускаем основную асинхронную функцию
EOF