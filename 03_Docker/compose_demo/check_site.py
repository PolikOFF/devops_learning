#!/usr/bin/env python3
"""
Мониторинг доступности сайтов для DevOps (постоянно + пишет в базу данных)
"""

import urllib.request
import urllib.error
import time
import datetime
import os
import psycopg2

SITES = [
    {"name": "Google", "url": "https://www.google.com"},
    {"name": "GitHub", "url": "https://github.com"},
    {"name": "Yandex", "url": "https://yandex.ru"},
    {"name": "HH", "url": "https://hh.ru"},
]

CHECK_INTERVAL = 30

DB_HOST = os.getenv('DB_HOST', 'db')
DB_NAME = os.getenv('POSTGRES_DB', 'monitoring')
DB_USER = os.getenv('POSTGRES_USER', 'monitor')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'secret123')

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )

def create_database():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS site_checks (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP NOT NULL,
            site_name VARCHAR(100) NOT NULL,
            site_url VARCHAR(500) NOT NULL,
            status VARCHAR(10) NOT NULL,
            response_time FLOAT,
            status_code INT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    cur.close()
    conn.close()
    print("✅ База данных инициализирована")

def save_to_db(timestamp, site_name, site_url, status, response_time, status_code):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO site_checks (timestamp, site_name, site_url, status, response_time, status_code)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (timestamp, site_name, site_url, status, response_time, status_code))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error saving data to DB: {e}")
        return False

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
    timestamp = datetime.datetime.now()
    timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
    print(f"\n{'='*50}")
    print(f"🕐 Проверка: {timestamp_str}")
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
        save_to_db(timestamp, name, url, status, response_time, status_code)

if __name__ == "__main__":
    print("🚀 DevOps Site Monitor - non-stop mode")
    print(f"⏱️  Checking interval: {CHECK_INTERVAL} sec")
    print(f"DataBase: {DB_HOST}/{DB_NAME}")
    try:
        create_database()
    except Exception as e:
        print(f"Error connection to DB: {e}")
        print("Work continues, information will not be saved!")
    print("For stop use Ctrl+C")
    try:
        while True:
            main()
            print(f"💤 Sleep at {CHECK_INTERVAL} seconds...")
            time.sleep(CHECK_INTERVAL)
    except KeyboardInterrupt:
        print("\n\n🛑 Monitoring stopped")
