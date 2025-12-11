from fastapi import FastAPI, Request, HTTPException
import requests
import json
import os
import logging
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import pytz
import re

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(title="AWX Telegram Webhook")

# Получаем конфигурацию из переменных окружения
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
AWX_BASE_URL = os.getenv("AWX_BASE_URL", "https://awx.example.com")

if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
    logger.error("TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID not set!")
    raise ValueError("Telegram credentials not configured")

def escape_html(text: str) -> str:
    """Экранирование HTML спецсимволов"""
    if not text:
        return ""
    return (text.replace("&", "&amp;")
                .replace("<", "&lt;")
                .replace(">", "&gt;")
                .replace('"', "&quot;"))

def normalize_url(url: Optional[str]) -> Optional[str]:
    """Нормализация URL - преобразует относительный URL в абсолютный"""
    if not url:
        return None
    
    # Убираем возможные пробелы
    url = url.strip()
    
    # Если URL уже полный (начинается с http:// или https://)
    if url.startswith(('http://', 'https://')):
        return url
    
    # Если это относительный путь (начинается с /)
    if url.startswith('/'):
        # Убираем дублирующие слэши
        base_url = AWX_BASE_URL.rstrip('/')
        relative_url = url.lstrip('/')
        return f"{base_url}/{relative_url}"
    
    # Если это просто путь без слэша
    if not url.startswith(('http://', 'https://', '/')):
        return f"{AWX_BASE_URL}/{url}"
    
    # Если это AWX URL формата #/jobs/playbook/55
    if url.startswith('#/'):
        # Преобразуем hash-based URL в нормальный
        # AWX часто использует URL вида: https://awx.example.com/#/jobs/playbook/55
        base_url = AWX_BASE_URL.rstrip('/')
        return f"{base_url}/{url.lstrip('#/')}"
    
    # Для hash navigation в AWX
    if '#/jobs/' in url or '#/jobs/playbook/' in url:
        base_url = AWX_BASE_URL.rstrip('/')
        return f"{base_url}/{url}"
    
    logger.warning(f"Не удалось нормализовать URL: {url}")
    return url

def convert_to_moscow_time(utc_time_str: Optional[str]) -> Optional[str]:
    """Конвертирует строку времени из UTC в московское время"""
    if not utc_time_str:
        return None
    
    try:
        # Парсим время
        if 'T' in utc_time_str:
            if utc_time_str.endswith('Z'):
                dt = datetime.fromisoformat(utc_time_str.replace('Z', '+00:00'))
            else:
                dt = datetime.fromisoformat(utc_time_str)
        else:
            for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f'):
                try:
                    dt = datetime.strptime(utc_time_str, fmt)
                    dt = dt.replace(tzinfo=timezone.utc)
                    break
                except ValueError:
                    continue
            else:
                logger.warning(f"Не удалось распарсить время: {utc_time_str}")
                return utc_time_str
        
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        
        moscow_tz = pytz.timezone('Europe/Moscow')
        moscow_time = dt.astimezone(moscow_tz)
        
        return moscow_time.strftime("%Y-%m-%d %H:%M:%S MSK")
    
    except Exception as e:
        logger.error(f"Ошибка конвертации времени {utc_time_str}: {e}")
        return utc_time_str

def send_telegram_message(text: str, parse_mode: str = "HTML") -> bool:
    """Отправка сообщения в Telegram"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": parse_mode,
        "disable_web_page_preview": False  # Разрешаем превью для корректных URL
    }
    
    logger.info(f"📤 Отправка в Telegram, chat_id: {TELEGRAM_CHAT_ID}")
    
    try:
        response = requests.post(url, json=payload, timeout=10)
        logger.info(f"Telegram API HTTP статус: {response.status_code}")
        
        result = response.json()
        
        if result.get("ok") == True:
            logger.info("✅ Сообщение отправлено в Telegram")
            return True
        else:
            error_msg = result.get("description", "Unknown error")
            logger.error(f"❌ Ошибка Telegram API: {error_msg}")
            return False
            
    except Exception as e:
        logger.error(f"💥 Ошибка отправки сообщения в Telegram: {e}")
        return False

def extract_job_id_from_url(url: str) -> Optional[int]:
    """Извлечение ID задачи из URL"""
    try:
        # Ищем ID в URL
        patterns = [
            r'/jobs/playbook/(\d+)',
            r'#/jobs/playbook/(\d+)',
            r'/jobs/(\d+)',
            r'#/jobs/(\d+)',
            r'/api/v2/jobs/(\d+)/'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return int(match.group(1))
        
        # Попробуем найти число в конце URL
        match = re.search(r'/(\d+)/?$', url)
        if match:
            return int(match.group(1))
            
    except Exception as e:
        logger.error(f"Ошибка извлечения ID из URL {url}: {e}")
    
    return None

def format_job_message(job_data: Dict[str, Any]) -> str:
    """Форматирование сообщения для Telegram"""
    
    status_icons = {
        "successful": "✅",
        "failed": "❌",
        "error": "🚨",
        "canceled": "⏹️",
        "running": "🔄",
        "pending": "⏳",
        "waiting": "⏳"
    }
    
    status = job_data.get("status", "unknown").lower()
    icon = status_icons.get(status, "📝")
    
    # Имя запустившего
    launched_by = "Неизвестно"
    launched_by_info = job_data.get("launched_by", {})
    if launched_by_info:
        username = launched_by_info.get("username", "Неизвестно")
        name_parts = []
        if launched_by_info.get("first_name"):
            name_parts.append(launched_by_info["first_name"])
        if launched_by_info.get("last_name"):
            name_parts.append(launched_by_info["last_name"])
        
        if name_parts:
            launched_by = f"{username} ({' '.join(name_parts)})"
        else:
            launched_by = username
    
    # Форматирование extra_vars
    extra_vars_text = "Нет переменных"
    extra_vars = job_data.get("extra_vars")
    if extra_vars:
        try:
            if isinstance(extra_vars, str):
                parsed_vars = json.loads(extra_vars)
            else:
                parsed_vars = extra_vars
            formatted_vars = json.dumps(parsed_vars, indent=2, ensure_ascii=False)
            if len(formatted_vars) > 1000:
                formatted_vars = formatted_vars[:1000] + "\n... (обрезано)"
            extra_vars_text = f"<pre>{escape_html(formatted_vars)}</pre>"
        except Exception as e:
            logger.error(f"Ошибка парсинга extra_vars: {e}")
            extra_vars_text = escape_html(str(extra_vars)[:500])
    
    # Конвертируем время
    started_msk = convert_to_moscow_time(job_data.get("started"))
    finished_msk = convert_to_moscow_time(job_data.get("finished"))
    
    # ПОЛУЧАЕМ ИЛИ ГЕНЕРИРУЕМ URL
    job_id = job_data.get("id")
    awx_base_url = AWX_BASE_URL.rstrip('/')
    
    # Формируем URL на основе ID
    if job_id and job_id != "N/A":
        # Стандартный URL для AWX задач
        job_url = f"{awx_base_url}/#/jobs/playbook/{job_id}"
        logger.info(f"📎 Сгенерирован URL: {job_url}")
    else:
        job_url = ""
        logger.warning("⚠️ Не удалось сгенерировать URL (отсутствует ID)")
    
    # Формируем сообщение
    message = f"""
{icon} <b>AWX Job: {escape_html(job_data.get('name', 'Неизвестно'))}</b>

<b>Статус:</b> {escape_html(status.upper())}
<b>ID:</b> {escape_html(str(job_id))}
<b>Запустил:</b> {escape_html(launched_by)}
"""
    
    # Дополнительные поля
    project = job_data.get("project")
    if project and project != 'N/A':
        message += f"<b>Проект:</b> {escape_html(project)}\n"
    
    inventory = job_data.get("inventory")
    if inventory and inventory != 'N/A':
        message += f"<b>Инвентарь:</b> {escape_html(inventory)}\n"
    
    playbook = job_data.get("playbook")
    if playbook and playbook != 'N/A':
        message += f"<b>Playbook:</b> {escape_html(playbook)}\n"
    
    # Переменные
    if extra_vars:
        message += f"\n<b>Переменные:</b>\n{extra_vars_text}\n"
    
    # Время
    if started_msk and finished_msk:
        message += f"\n<b>Время:</b> {escape_html(started_msk)} - {escape_html(finished_msk)}"
    elif started_msk:
        message += f"\n<b>Запущено:</b> {escape_html(started_msk)}"
    
    # Ссылка на job - ОБЯЗАТЕЛЬНО с полным URL
    if job_url:
        # ВАЖНО: URL должен быть абсолютным и начинаться с https://
        if job_url.startswith(('http://', 'https://')):
            message += f"\n\n🔗 <a href=\"{escape_html(job_url)}\">Открыть в AWX</a>"
        else:
            # Если почему-то URL не абсолютный, делаем его таковым
            full_url = f"{awx_base_url}/{job_url.lstrip('/')}"
            message += f"\n\n🔗 <a href=\"{escape_html(full_url)}\">Открыть в AWX</a>"
    else:
        message += f"\n\n⚠️ Ссылка на задачу недоступна"
    
    return message

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "awx-telegram-webhook", "timestamp": datetime.now().isoformat()}

@app.get("/config")
async def show_config():
    return {
        "telegram_token_set": bool(TELEGRAM_BOT_TOKEN),
        "telegram_chat_id": TELEGRAM_CHAT_ID,
        "awx_base_url": AWX_BASE_URL,
        "timestamp": datetime.now().isoformat()
    }

@app.post("/webhook")
async def receive_webhook(request: Request):
    logger.info("=" * 60)
    logger.info("📨 ПОЛУЧЕН ВЕБХУК ОТ AWX")
    
    try:
        data = await request.json()
        logger.info(f"📊 Ключи данных: {list(data.keys())}")
        
        # Базовые данные задачи
        job_data = {
            "id": data.get("id") or data.get("unified_job_id", 0),
            "name": data.get("name", "Неизвестная задача"),
            "status": data.get("status", "unknown").lower(),
            "started": data.get("started"),
            "finished": data.get("finished"),
            "url": data.get("url", "")
        }
        
        # Пользователь
        summary_fields = data.get("summary_fields", {})
        
        # Определяем пользователя
        user_info = None
        user_sources = [
            summary_fields.get("created_by"),
            summary_fields.get("user"),
            summary_fields.get("job", {}).get("launched_by"),
            data.get("created_by"),
            data.get("launched_by")
        ]
        
        for source in user_sources:
            if source:
                if isinstance(source, dict):
                    user_info = {
                        "username": source.get("username", ""),
                        "first_name": source.get("first_name", ""),
                        "last_name": source.get("last_name", "")
                    }
                    break
                elif isinstance(source, str):
                    user_info = {"username": source}
                    break
        
        if user_info:
            job_data["launched_by"] = user_info
        
        # Extra vars
        if "extra_vars" in data:
            job_data["extra_vars"] = data["extra_vars"]
        
        # Дополнительные поля
        if summary_fields.get("project"):
            job_data["project"] = summary_fields["project"].get("name", "")
        
        if summary_fields.get("inventory"):
            job_data["inventory"] = summary_fields["inventory"].get("name", "")
        
        if "playbook" in data:
            job_data["playbook"] = data["playbook"]
        elif summary_fields.get("playbook"):
            job_data["playbook"] = summary_fields["playbook"]
        
        logger.info(f"📋 Обработанные данные: {job_data}")
        
        # Форматируем и отправляем
        message = format_job_message(job_data)
        logger.info(f"📝 Форматированное сообщение ({len(message)} символов)")
        
        success = send_telegram_message(message)
        
        if success:
            logger.info("✅ Уведомление отправлено в Telegram")
            logger.info("=" * 60)
            return {"ok": True, "status": "success", "message": "Notification sent to Telegram"}
        else:
            logger.error("❌ Не удалось отправить уведомление в Telegram")
            logger.info("=" * 60)
            return {"ok": False, "status": "error", "message": "Failed to send to Telegram"}
            
    except Exception as e:
        logger.error(f"💥 Ошибка обработки вебхука: {e}", exc_info=True)
        logger.info("=" * 60)
        return {"ok": False, "error": str(e)}

@app.post("/test")
async def test_webhook():
    """Тестовый endpoint"""
    test_data = {
        "id": 55,
        "name": "Тестовая задача AWX",
        "status": "successful",
        "started": "2025-12-10T07:49:02.123456Z",
        "finished": "2025-12-10T07:49:08.654321Z",
        "launched_by": {
            "username": "n.bayov",
            "first_name": "Nikolay",
            "last_name": "Bayov"
        },
        "project": "Test Project",
        "inventory": "Production",
        "playbook": "test.yml",
        "extra_vars": {"ansible_user": "ansible", "ansible_become": True},
        "url": "#/jobs/playbook/55"
    }
    
    message = format_job_message(test_data)
    success = send_telegram_message(message)
    
    return {
        "test_sent": success,
        "message_preview": message[:100],
        "config": {
            "awx_base_url": AWX_BASE_URL,
            "chat_id": TELEGRAM_CHAT_ID
        }
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)