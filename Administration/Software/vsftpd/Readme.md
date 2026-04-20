# Создание ftp сервера, для внешнего и локального доступа(debian13)

### Устанавливаем vsftpd
```
apt install vsftpd
```
### Настраиваем конфиги для внешки и локалки

```
sudo nano /etc/vsftpd-external.conf
```
```
listen=YES
listen_ipv6=NO
listen_address={{your_external_ip}}
listen_port=222

anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022

dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=NO

pam_service_name=vsftpd
secure_chroot_dir=/var/run/vsftpd/empty

chroot_local_user=YES

userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO

pasv_enable=YES
pasv_min_port=50000
pasv_max_port=50050
pasv_address={{your_external_ip}}
seccomp_sandbox=NO
log_ftp_protocol=YES
vsftpd_log_file=/var/log/vsftpd-external.log

ssl_enable=NO
```

```
sudo nano /etc/vsftpd-internal.conf
```


```
listen=YES
listen_ipv6=NO
listen_address={{your_internal_ip}}
listen_port=223

anonymous_enable=NO
local_enable=YES
write_enable=YES
local_umask=022

dirmessage_enable=YES
use_localtime=YES
xferlog_enable=YES
connect_from_port_20=NO

pam_service_name=vsftpd
secure_chroot_dir=/var/run/vsftpd/empty

chroot_local_user=YES

userlist_enable=YES
userlist_file=/etc/vsftpd.userlist
userlist_deny=NO

pasv_enable=YES
pasv_min_port=50051
pasv_max_port=50100
pasv_address={{your_internal_ip}}

seccomp_sandbox=NO
log_ftp_protocol=YES
vsftpd_log_file=/var/log/vsftpd-internal.log

ssl_enable=NO
```

### После подключаем наши конфиги в systemd-unit

```
sudo cp /lib/systemd/system/vsftpd.service /etc/systemd/system/vsftpd-external.service
sudo cp /lib/systemd/system/vsftpd.service /etc/systemd/system/vsftpd-internal.service
```
### меняем строку с 
/etc/systemd/system/vsftpd-external.service
`ExecStart=/usr/sbin/vsftpd /etc/vsftpd.conf` --> `ExecStart=/usr/sbin/vsftpd /etc/vsftpd-external.conf`
/etc/systemd/system/vsftpd-internal.service
`ExecStart=/usr/sbin/vsftpd /etc/vsftpd.conf` --> `ExecStart=/usr/sbin/vsftpd /etc/vsftpd-internal.conf`

### Создаём файлы логов
```
sudo touch /var/log/vsftpd-external.log /var/log/vsftpd-internal.log
sudo chmod 644 /var/log/vsftpd-external.log /var/log/vsftpd-internal.log
```
### Подключаем systemd юниты
```
sudo systemctl enable --now vsftpd-external
sudo systemctl enable --now vsftpd-internal
```

### Проверяем работу vsftpd
```
sudo systemctl status vsftpd-external --no-pager
sudo systemctl status vsftpd-internal --no-pager
sudo ss -tulpen | grep -E '222|223'
```
