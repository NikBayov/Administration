# Приложение для отображения totp QR-кода в удобном web-интерфейсе

![screenshot](/cache/picture/web-qr.png)

### Принцип работы
```
1) Приложение написано на python;
2) В качестве веб-сервера используется nginx;
3) Приложение разворачивается в docker;
4) Приложение запрашивает у пользователя логин и пароль ldap, если данные верны выводит QR-code который зараннее сгенерирован с помощью скрипта /etc/openvpn/oath-secret-gen.sh
5) Если пароль или логин неверны,приложение вернёт ошибку
```
![screenshot](/cache/picture/web-qr1.png)

## Установка и настройка приложения

### Устанавливаем Docker

```
apt update
apt install docker.io docker-compose
```

### Скачиваем архив приложения

```
wget https://github.com/NikBayov/Administration/blob/main/cache/archives/web-qr-docker.zip
unzip web-qr-docker.zip
cd web-qr-docker
```
### Редактируем конфиги 

##### Редактируем app.py
```
1) Приписываем свой ldap сервер в web-qr-docker/app/app.py;
2) Добавляем сгенерированные qr-коды в папку web-qr-docker/app/static/qr-klients/
```
##### Редактируем nginx
```
1) Меняем домены и ключи на свои в web-qr-docker/nginx/
```

### Запускаем приложение
```
cd web-qr-docker
docker-compose build
docker-compose up -d
```
