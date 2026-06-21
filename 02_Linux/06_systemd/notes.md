# Linux Systemd

## Команды
| Команда | Назначение |
|---------|------------|
| `systemctl status name` | статус сервиса |
| `systemctl start name` | запустить |
| `systemctl stop name` | остановить |
| `systemctl restart name` | перезапустить |
| `systemctl enable name` | автозапуск |
| `systemctl disable name` | убрать автозапуск |
| `journalctl -u name` | логи сервиса |

## Unit-файл
- `/etc/systemd/system/` — пользовательские сервисы
- `/lib/systemd/system/` — системные сервисы

Описание Unit-файла:

[Unit]
Description=Название
After=network.target - порядок запуска, обозначает что службу нужно запускать когда сеть готова

[Service]
ExecStart=Путь к скрипту
Restart=перезапуск (always)
User=имя_пользователя

[Install]
WantedBy=указывает, что служба привязана к стандартному режиму загрузки Linux (многопользовательский режим без графики или с ней). 
Именно эта строчка позволяет команде sudo systemctl enable понять, куда прописать службу, чтобы она автоматически стартовала при включении компьютера.
