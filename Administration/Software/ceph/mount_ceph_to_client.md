# Монтирование ceph к клиентскому хосту

## Копируем конфиги и ключи с кластера ceph
#### `ceph1@root`
```
scp -r /etc/ceph/* client_host:/etc/ceph/
```
## Client host
```
apt install ceph-fuse

ceph-fuse -m ceph1_ip:6789 /mnt/cephfs --id admin  -d --no-mon-config
```
### ИЛИ
```
apt install ceph-common
mount -t ceph :/pg1 /mnt/pgdata -o name=admin,fs=cephfs-db
```
### Проверяем примонтировался ли volume
```
ls -la /mnt/cephfs
```
