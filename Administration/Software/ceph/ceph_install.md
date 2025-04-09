# Установка Ceph-кластера из 3-х вм на debian12

|       Ceph1      |      Ceph2      |      Ceph3     |
|------------------|-----------------|----------------|
| 192.168.0.110    | 192.168.0.111   | 192.168.0.112  |

### Устанавливаем необзодимые пакеты на всех вм
```
apt install gpg curl chrony sudo
```
### Прописываем хосты на всех вм
```
192.168.0.110 ceph1
192.168.0.111 ceph2
192.168.0.112 ceph3
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
### Открываем веб-интерфейс
#### В выводе команды получаем логин и пароль  для первого входа и смены пароля
`Адрес для входа: https://172.17.28.41:8443`
### Установка Ceph CLI (на всех ВМ)
```
apt install ceph-common
```
### Добавляем ключ /etc/ceph/ceph.pub с ceph1 на ceph2,ceph3
### Инициализация ВМ в кластере(ceph1):
```
ceph orch host add ceph2

ceph orch host add ceph3

Лейблы:

ceph orch host label add ceph2 mon

ceph orch host label add ceph3 mon

ceph orch host label add ceph2 osd

ceph orch host label add ceph3 osd
```
### Включение mds(ceph1):
```
ceph orch apply mds cephfs --placement="3 ceph1 ceph2 ceph3"
```
### Включение и проверка имеющихся разделов диска в osd(ceph1):
```
ceph orch apply osd --all-available-devices --method lvm
ceph orch device ls
```
