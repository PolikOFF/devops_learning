#!/usr/bin/env python3
"""
Мониторинг доступности сайтов для DevOps
Проверяет сайты и отправляет уведомления при проблемах
"""

import urllib.request
import urllib.error
import json
import time
import datetime
import os

# Конфигурация
SITES = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Yandex", "url": "https://yandex.ru"},
    {"name": "HH", "url": "https://hh.ru"},
]

# Telegram настройки (заполните позже)
TELEGRAM_BOT_TOKEN = ""  # Токен бота от @BotFather
TELEGRAM_CHAT_ID = ""     # Ваш chat_id

# Файл для истории проверок
HISTORY_FILE = "site_history.json"

def send_telegram(message):
    """Отправляет сообщение в Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return  # Telegram не настроен
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        urllib.request.urlopen(req, timeout=10)
    except Exception as e:
        print(f"❌ Ошибка отправки в Telegram: {e}")

def check_site(name, url):
    """
    Проверяет доступность сайта
    Возвращает: (status, response_time, status_code)
    """
    try:
        start_time = time.time()
        req = urllib.request.Request(
            url,
            headers={'User-Agent': 'DevOps-Monitor/1.0'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            response_time = time.time() - start_time
            status_code = response.getcode()
            
            if 200 <= status_code < 400:
                status = "UP"
            else:
                status = "DOWN"
                
            return status, round(response_time, 2), status_code
            
    except urllib.error.HTTPError as e:
        return "DOWN", 0, e.code
    except urllib.error.URLError as e:
        return "DOWN", 0, str(e)
    except Exception as e:
        return "DOWN", 0, str(e)

def save_to_history(data):
    """Сохраняет результаты проверки в файл"""
    history = []
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            history = json.load(f)
    
    history.append(data)
    
    # Оставляем только последние 100 записей
    if len(history) > 100:
        history = history[-100:]
    
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=2)

def get_stats():
    """Показывает статистику из истории"""
    if not os.path.exists(HISTORY_FILE):
        print("📭 Нет истории проверок")
        return
    
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)
    
    if not history:
        return
    
    print(f"\n📊 Статистика за последние {len(history)} проверок:")
    
    # Статистика по каждому сайту
    for site_name in [s["name"] for s in SITES]:
        site_checks = [h for h in history if h["site"] == site_name]
        if site_checks:
            up_count = sum(1 for h in site_checks if h["status"] == "UP")
            up_percent = (up_count / len(site_checks)) * 100
            avg_time = sum(h["response_time"] for h in site_checks if h["response_time"] > 0) / len(site_checks)
            print(f"   {site_name}: {up_percent:.1f}% доступен (ср. ответ: {avg_time:.2f}с)")

def main():
    print("=" * 50)
    print("🌐 DevOps Site Monitor v1.0")
    print("=" * 50)
    
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n🕐 Время проверки: {timestamp}")
    
    failed_sites = []
    
    for site in SITES:
        name = site["name"]
        url = site["url"]
        
        print(f"\n🔍 Проверка {name} ({url})...", end=" ", flush=True)
        
        status, response_time, status_code = check_site(name, url)
        
        if status == "UP":
            print(f"✅ UP ({response_time}с, код {status_code})")
        else:
            print(f"❌ DOWN (ошибка: {status_code})")
            failed_sites.append(f"• {name}: {status_code}")
        
        # Сохраняем в историю
        save_to_history({
            "timestamp": timestamp,
            "site": name,
            "url": url,
            "status": status,
            "response_time": response_time,
            "status_code": status_code if isinstance(status_code, int) else 0
        })
    
    # Отправляем уведомление, если есть проблемы
    if failed_sites:
        message = f"⚠️ <b>ALERT: Проблемы с доступностью</b>\n{timestamp}\n\n" + "\n".join(failed_sites)
        send_telegram(message)
        print(f"\n📨 Отправлено уведомление о {len(failed_sites)} проблемах")
    else:
        print("\n✅ Все сайты доступны!")
    
    # Показываем статистику
    get_stats()
    
    print("\n" + "=" * 50)
    print("💡 Для постоянного мониторинга используйте cron или systemd timer")
    print("=" * 50)

if __name__ == "__main__":
    main()
