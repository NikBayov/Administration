### Для смены пула ip-адресов создаём файл /etc/docker/daemon.json
```
{
  "default-address-pools": [
    {
      "base": "10.200.0.0/16",
      "size": 24
    }
  ]
}
```
### Удаляем подсети

```
cd /etc/docker
docker compose down
docker network prune
docker compose up -d
```
### После перезапускаем контейнеры
```
docker-compose down
docker-compose up -d
```
