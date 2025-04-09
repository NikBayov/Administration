# Установка Ceph-кластера из 3-х вм на debian12

|       Ceph1      |      Ceph2      |      Ceph3     |
|------------------|-----------------|----------------|
| 192.168.0.110    | 192.168.0.111   | 192.168.0.112  |

### Устанавливаем необзодимые пакеты на всех вм
```
apt install gpg curl chrony sudo
```
### на всех вм 
```
apt-cache policy cephadm
```
### Добавляем реп на всех вм
```
wget -q -O- 'https://download.ceph.com/keys/release.asc' | \
gpg --dearmor -o /etc/apt/trusted.gpg.d/cephadm.gpg

echo deb https://download.ceph.com/debian-reef/ $(lsb_release -sc) main \
> /etc/apt/sources.list.d/ceph.list

apt update
```

### Выполняем
```
apt-cache policy cephadm 
```
### Устанавливаем на всех вм
```
apt install cephadm
```
### Инициализируем Cluster monitor на ceph1
```
cephadm bootstrap --mon-ip 192.168.0.110
```
### 
#### В выводе команды получаем логин и пароль  для первого входа и смены пароля
`Адрес для входа: https://172.17.28.41:8443`
