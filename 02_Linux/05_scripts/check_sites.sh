#!/bin/bash
# Проверка доступности сайтов (аналог Python-скрипта)

SITES=("google.com" "vk.com" "yandex.ru" "hh.ru")
DATE=$(date '+%Y-%m-%d %H:%M:%S')

echo "🕐 Проверка: $DATE"
echo "==============================="

for SITE in "${SITES[@]}"; do
    if ping -c 1 -W 2 "$SITE" &>/dev/null; then
        echo "✅ $SITE — доступен"
    else
        echo "❌ $SITE — НЕ ДОСТУПЕН"
    fi
done
