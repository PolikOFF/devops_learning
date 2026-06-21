#!/usr/bin/env python3
"""
Мониторинг доступности сайтов для CI (без БД)
"""

import urllib.request
import urllib.error
import time

SITES = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Yandex", "url": "https://yandex.ru"},
    {"name": "HH", "url": "https://hh.ru"},
]

def check_site(name, url):
    try:
        start_time = time.time()
        req = urllib.request.Request(url, headers={'User-Agent': 'DevOps-Monitor/1.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            response_time = time.time() - start_time
            status_code = response.getcode()
            status = "UP" if 200 <= status_code < 400 else "DOWN"
            return status, round(response_time, 2), status_code
    except Exception as e:
        return "DOWN", 0, 0

def main():
    print(f"\n{'='*50}")
    print("🕐 CI Проверка сайтов")
    print(f"{'='*50}")
    
    for site in SITES:
        name = site["name"]
        url = site["url"]
        print(f"[CHECK] {name}...", end=" ", flush=True)
        status, response_time, status_code = check_site(name, url)
        if status == "UP":
            print(f"✅ UP ({response_time}с, {status_code})")
        else:
            print(f"❌ DOWN (ошибка: {status_code})")

if __name__ == "__main__":
    main()

