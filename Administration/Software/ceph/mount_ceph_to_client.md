# Монтирование ceph к клиентскому хосту
#### `ceph1@root`
```
scp -r /etc/ceph/* client_host:/etc/ceph/
```
## Client host
```
apt install ceph-fuse

ceph-fuse -m ceph1_ip:6789 /mnt/cephfs --id admin  -d --no-mon-config
```
