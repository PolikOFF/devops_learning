#!/bin/bash
# Простой скрипт для бэкапа логов

BACKUP_DIR="$HOME/backups"
LOG_DIR="/var/log"
DATE=$(date +%Y-%m-%d_%H-%M-%S)

# Создаём папку для бэкапов
mkdir -p "$BACKUP_DIR"

# Копируем логи
cp -r "$LOG_DIR" "$BACKUP_DIR/logs_$DATE"

echo "✅ Бэкап создан: $BACKUP_DIR/logs_$DATE"
echo "📊 Размер: $(du -sh "$BACKUP_DIR/logs_$DATE" | cut -f1)"
