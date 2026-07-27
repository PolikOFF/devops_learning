#!/usr/bin/env python3
import time
import datetime
import os
import psycopg2
import requests

SITES = [
    {"name": "Google", "url": "http://www.google.com"},
    {"name": "GitHub", "url": "http://github.com"},
    {"name": "Yandex", "url": "http://yandex.ru"},
    {"name": "HH", "url": "http://hh.ru"},
]

CHECK_INTERVAL = 30

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('POSTGRES_DB', 'monitoring')
DB_USER = os.getenv('POSTGRES_USER', 'monitor')
DB_PASS = os.getenv('POSTGRES_PASSWORD', 'secret123')

def get_db_connection():
    return psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASS)

def create_database():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
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
    print("✅ База данных инициализирована")

def save_to_db(timestamp, site_name, site_url, status, response_time, status_code):
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO site_checks (timestamp, site_name, site_url, status, response_time, status_code)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (timestamp, site_name, site_url, status, response_time, status_code))
                conn.commit()
        return True
    except Exception as e:
        print(f"Error saving data to DB: {e}")
        return False

def check_site(name, url):
    try:
        start = time.time()
        response = requests.get(url, timeout=10)
        elapsed = time.time() - start
        if 200 <= response.status_code < 400:
            return "UP", round(elapsed, 2), response.status_code
        return "DOWN", round(elapsed, 2), response.status_code
    except Exception:
        return "DOWN", 0, 0

def main():
    timestamp = datetime.datetime.now()
    print(f"\n{'='*50}")
    print(f"🕐 Проверка: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*50}")
    for site in SITES:
        status, response_time, status_code = check_site(site["name"], site["url"])
        print(f"[CHECK] {site['name']}... {'✅' if status == 'UP' else '❌'} {status} ({response_time}с, {status_code})")
        save_to_db(timestamp, site["name"], site["url"], status, response_time, status_code)

if __name__ == "__main__":
    print("🚀 DevOps Site Monitor - non-stop mode")
    print(f"⏱️  Checking interval: {CHECK_INTERVAL} сек")
    try:
        create_database()
    except Exception as e:
        print(f"Error creating table: {e}")
    print("Для остановки нажмите Ctrl+C")
    while True:
        main()
        time.sleep(CHECK_INTERVAL)
