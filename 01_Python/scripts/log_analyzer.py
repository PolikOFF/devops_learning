#!/usr/bin/env python3
"""
Анализатор логов для DevOps
Читает файл лога и выводит статистику по ошибкам
"""

import re
from collections import Counter
from datetime import datetime

def analyze_logs(filename):
    """
    Анализирует лог-файл и выводит статистику ошибок
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"❌ Файл {filename} не найден!")
        return
    except Exception as e:
        print(f"❌ Ошибка при чтении файла: {e}")
        return
    
    print(f"\n📊 Анализ файла: {filename}")
    print(f"📄 Всего строк в логе: {len(lines)}")
    
    # Паттерны для поиска ошибок
    error_patterns = [
        r'ERROR',
        r'CRITICAL',
        r'FATAL',
        r'Exception',
        r'Traceback'
    ]
    
    # Поиск ошибок в каждой строке
    errors = []
    error_messages = []
    
    for line_num, line in enumerate(lines, 1):
        for pattern in error_patterns:
            if re.search(pattern, line, re.IGNORECASE):
                errors.append({
                    'line_num': line_num,
                    'line': line.strip(),
                    'pattern': pattern
                })
                error_messages.append(line.strip())
                break
    
    # Статистика
    print(f"\n⚠️  Найдено ошибок: {len(errors)}")
    
    if not errors:
        print("✅ Ошибок не найдено! Лог чист.")
        return
    
    # Самые частые ошибки
    error_counter = Counter(error_messages)
    print("\n🔝 Топ-3 самых частых ошибок:")
    for i, (error, count) in enumerate(error_counter.most_common(3), 1):
        # Обрезаем длинные сообщения
        short_error = error[:80] + "..." if len(error) > 80 else error
        print(f"   {i}. [{count} раз] {short_error}")
    
    # Последние 5 ошибок
    print("\n⏱️  Последние 5 ошибок (по порядку):")
    last_errors = errors[-5:] if len(errors) > 5 else errors
    for err in last_errors:
        print(f"   Строка {err['line_num']}: {err['pattern']}")
        print(f"      {err['line'][:100]}")
    
    # Дополнительная информация
    error_by_type = Counter([e['pattern'] for e in errors])
    print("\n📊 Распределение по типам:")
    for error_type, count in error_by_type.most_common():
        print(f"   {error_type}: {count}")

def generate_sample_log():
    """
    Создаёт пример лог-файла для тестирования
    """
    sample_log = """2026-06-05 10:15:30 INFO Starting application
2026-06-05 10:15:31 DEBUG Loading configuration
2026-06-05 10:15:32 ERROR Database connection failed: timeout
2026-06-05 10:15:33 WARNING Retry attempt 1/3
2026-06-05 10:15:35 ERROR Database connection failed: timeout
2026-06-05 10:15:36 CRITICAL Application crashed: unable to recover
2026-06-05 10:15:37 ERROR Failed to send notification: SMTP error
2026-06-05 10:15:38 INFO Shutting down
2026-06-05 10:15:39 ERROR Database connection failed: timeout
2026-06-05 10:15:40 Exception in thread Thread-1: division by zero
2026-06-05 10:15:41 FATAL Out of memory
2026-06-05 10:15:42 ERROR Failed to send notification: SMTP error
2026-06-05 10:15:43 Traceback (most recent call last):
2026-06-05 10:15:44 ERROR Connection refused by backend
"""
    
    with open('sample.log', 'w', encoding='utf-8') as f:
        f.write(sample_log)
    print("✅ Создан пример лог-файла: sample.log")

def main():
    print("=" * 50)
    print("📋 DevOps Log Analyzer v1.0")
    print("=" * 50)
    
    # Создаём пример лога для теста
    generate_sample_log()
    
    # Анализируем лог
    analyze_logs('sample.log')
    
    print("\n" + "=" * 50)
    print("💡 Совет: Замените 'sample.log' на путь к вашему лог-файлу")
    print("=" * 50)

if __name__ == "__main__":
    main()
