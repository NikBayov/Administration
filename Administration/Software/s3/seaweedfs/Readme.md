# Установка seaweedfs для s3 хранилища на ВМ Debian13
!https://github.com/seaweedfs/seaweedfs#quick-start

### Подготавливаемся к установке 
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget unzip
sudo apt install -y lvm2
```

### Минимум надо два диска 1-для ОС другой для хранилища. У меня lvm на ext4
```
/dev/sda ---> OS
/dev/sdb ---> S3
```
#### Создаём lvm и проверям
```
pvcreate /dev/sdb
vgcreate vg_s3 /dev/sdb
lvcreate -n lv_seaweedfs -l 100%FREE vg_s3
lvs
```
#### Форматирует диск под файловую систему
```
mkfs.ext4 /dev/vg_s3/lv_seaweedfs
mkdir -p /data/seaweedfs
```
#### Смотрим id тома и добавляем его в fstab
```
blkid /dev/vg_s3/lv_seaweedfs
nano /etc/fstab
```
#### Монтируемся
```
mount -a
```
### Как должно быть поитогу
```
root@seaweedfs:~# lsblk -l
NAME                 MAJ:MIN RM  SIZE RO TYPE MOUNTPOINTS
sda                    8:0    0   20G  0 disk
sda1                   8:1    0  966M  0 part /boot
sda2                   8:2    0    1K  0 part
sda5                   8:5    0 19.1G  0 part
sdb                    8:16   0  100G  0 disk
sr0                   11:0    1 1024M  0 rom
seaweedfs--vg-root   254:0    0   18G  0 lvm  /
seaweedfs--vg-swap_1 254:1    0    1G  0 lvm  [SWAP]
vg_s3-lv_seaweedfs   254:2    0  100G  0 lvm  /data/seaweedfs
root@seaweedfs:~# df -h
Filesystem                      Size  Used Avail Use% Mounted on
udev                            2.9G     0  2.9G   0% /dev
tmpfs                           590M  1.1M  589M   1% /run
/dev/mapper/seaweedfs--vg-root   18G  1.9G   15G  12% /
tmpfs                           2.9G     0  2.9G   0% /dev/shm
tmpfs                           5.0M     0  5.0M   0% /run/lock
tmpfs                           1.0M     0  1.0M   0% /run/credentials/systemd-journald.service
tmpfs                           2.9G  212K  2.9G   1% /tmp
/dev/sda1                       933M  125M  745M  15% /boot
tmpfs                           1.0M     0  1.0M   0% /run/credentials/getty@tty1.service
tmpfs                           590M  8.0K  590M   1% /run/user/0
/dev/mapper/vg_s3-lv_seaweedfs   98G  2.2M   93G   1% /data/seaweedfs
overlay                          18G  1.9G   15G  12% /var/lib/docker/overlay2/ffc973a4221806ec00f788d0834778c5827bf6f42c843fb0deddf4cd75ffd7d7/merged
```

### Скачиваем seaweedfs

```
wget https://github.com/seaweedfs/seaweedfs/releases/latest/download/linux_amd64.tar.gz
tar -xzf linux_amd64.tar.gz
sudo mv weed /usr/local/bin/
```

### Проверяем установку 

```
weed version
```
### Делаем авторизацию для S3
```
cat > /etc/seaweedfs/s3.json <<'EOF'
{
  "identities": [
    {
      "name": "admin",
      "credentials": [
        {
          "accessKey": "seaweed-admin",
          "secretKey": "your_passwd"
        }
      ],
      "actions": [
        "Admin",
        "Read",
        "List",
        "Tagging",
        "Write"
      ]
    }
  ]
}
EOF
```
### Создаём скрипт запуска /usr/local/bin/start-seaweedfs.sh
```
#!/bin/bash

mkdir -p /data/seaweedfs/{master,volume,filer}
mkdir -p /var/log/seaweedfs

/usr/local/bin/weed master \
  -mdir=/data/seaweedfs/master \
  -ip=127.0.0.1 \
  -ip.bind=127.0.0.1 \
  -port=9333 \
  -defaultReplication=000 \
  > /var/log/seaweedfs/master.log 2>&1 &

sleep 5

/usr/local/bin/weed volume \
  -dir=/data/seaweedfs/volume \
  -ip=127.0.0.1 \
  -ip.bind=127.0.0.1 \
  -port=8080 \
  -mserver=172.17.33.111:9333 \
  -max=10 \
  > /var/log/seaweedfs/volume.log 2>&1 &

sleep 5

/usr/local/bin/weed filer \
  -ip=127.0.0.1 \
  -port=8888 \
  -master=127.0.0.1:9333 \
  > /var/log/seaweedfs/filer.log 2>&1 &

sleep 5

exec /usr/local/bin/weed s3 \
  -ip.bind=0.0.0.0 \
  -port=8333 \
  -filer=127.0.0.1:8888 \
  -config=/etc/seaweedfs/s3.json \
  > /var/log/seaweedfs/s3.log 2>&1
```
#### Создаём systemd-service /etc/systemd/system/seaweedfs.service
```
[Unit]
Description=SeaweedFS
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/local/bin/start-seaweedfs.sh
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target

```
```
systemctl daemon-reload
systemctl reset-failed seaweedfs
systemctl enable --now seaweedfs
systemctl status seaweedfs --no-pager
```
### Для GUI делаю авторизаиию через htpasswd и nginx(у меня docker)
```
apt install -y docker.io apache2-utils
```
#### Создаём пользователя 
```
mkdir -p /opt/seaweedfs-nginx/{conf,auth,ssl}
htpasswd -c /opt/seaweedfs-nginx/auth/.htpasswd admin
```
#### Надо минимум два домена, а то оснастка режется
```
s3.examle.ru
s3-api.exapmle.ru
```
#### Создаём конфиг nginx
```
cat > /opt/seaweedfs-nginx/conf/default.conf <<'EOF'
server {
    listen 80;
    server_name s3.examle.ru s3-api.examle.ru;

    return 301 https://$host$request_uri;
}

#
# GUI
#
server {
    listen 443 ssl;
    server_name s3.examle.ru;

    ssl_certificate     /etc/nginx/ssl/tls.crt;
    ssl_certificate_key /etc/nginx/ssl/tls.key;

    auth_basic "SeaweedFS Admin";
    auth_basic_user_file /etc/nginx/auth/.htpasswd;

    location /master/ {
        proxy_pass http://host.docker.internal:9333/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }

    location / {
        proxy_pass http://host.docker.internal:8888/;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;
    }
}

#
# S3 API
#
server {
    listen 443 ssl;
    server_name s3-api.examle.ru;

    ssl_certificate     /etc/nginx/ssl/tls.crt;
    ssl_certificate_key /etc/nginx/ssl/tls.key;

    client_max_body_size 0;

    location / {
        auth_basic off;

        proxy_pass http://host.docker.internal:8333;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-Proto https;

        proxy_request_buffering off;
        proxy_buffering off;
    }
}
EOF
```

### Запускаем nginx 
```
docker run -d \
  --name seaweedfs-nginx \
  --restart unless-stopped \
  --add-host=host.docker.internal:host-gateway \
  -p 80:80 \
  -p 443:443 \
  -v /opt/seaweedfs-nginx/conf/default.conf:/etc/nginx/conf.d/default.conf:ro \
  -v /opt/seaweedfs-nginx/auth/.htpasswd:/etc/nginx/auth/.htpasswd:ro \
  -v /opt/seaweedfs-nginx/ssl:/etc/nginx/ssl:ro \
  nginx:alpine
```
### Проверяем доступ к gui и s3
![screenshot](/cache/picture/s3-filer-seaweedfs.png)
![screenshot](/cache/picture/s3-master-seaweedfs.png)

### Доступ к s3 через cli aws
```
apt update
apt install -y awscli
```
#### Настраиваем AWS CLI профиль
```
aws configure --profile seaweedfs-admin
```
```
AWS Access Key ID: seaweed-admin
AWS Secret Access Key: your_passwd
Default region name: us-east-1
Default output format: json
```
#### Проверяем подключение 
```
aws --profile seaweedfs-admin   --endpoint-url https://s3-api.example.ru   s3 mb s3://test-bucket
aws --profile seaweedfs-admin   --endpoint-url https://s3-api.example.rus s3 cp test.txt s3://test-bucket/
aws --profile seaweedfs-admin   --endpoint-url https://s3-api.example.ru   s3 ls s3://test-bucket
```
#### Должны получить
```
2026-05-26 16:04:32         16 test.txt
```
