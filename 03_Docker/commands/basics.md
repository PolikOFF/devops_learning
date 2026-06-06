# Мои первые Docker-команды

## Запустить Nginx
docker run -d --name test-nginx -p 8080:80 nginx

## Проверить работу
docker ps
# Открыть в браузере: http://localhost:8080

## Остановить
docker stop test-nginx

## Запустить снова
docker start test-nginx

## Удалить
docker rm test-nginx
