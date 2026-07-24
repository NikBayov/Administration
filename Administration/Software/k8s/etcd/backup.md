# Создание backup etcd

### Создаём бэкап через cli
```
mkdir -p /var/backups/etcd/
chmod 700 /var/backups/etcd/
```
```
BACKUP="/var/backups/etcd/etcd-$(date +%Y-%m-%d_%H-%M-%S).db"

etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert="$ETCD_CA" \
  --cert="$ETCD_CERT" \
  --key="$ETCD_KEY" \
  snapshot save "$BACKUP"

```
### Проверяем целостность 
```
etcdutl snapshot status "$BACKUP" -w table
```
#### Должно быть примерно 
```
+----------+----------+------------+------------+---------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE | VERSION |
+----------+----------+------------+------------+---------+
| 93c1c664 |  2695668 |        950 |      60 MB |   3.6.0 |
+----------+----------+------------+------------+---------+
```
