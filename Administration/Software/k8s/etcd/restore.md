# Востановление etcd в кластере k8s(kubespray)
+----------+----------+------------------+
|    etcd1    |    etcd2    |    etcd3   |
+----------+----------+------------------+
| 192.168.1.1 | 192.168.1.2 | 192.168.1.3|
+----------+----------+------------------+
### Предварительно мы должны иметь бэкап бд etcd

```
root@s-app-k8s-mn01:~# ls -lh "$BACKUP"
-rw------- 1 root root 58M Jul 24 10:40 /var/backups/etcd/etcd-2026-07-24_10-40-35.db
```

### Проверяем целостность бэкапа
```
etcdutl snapshot status /var/backups/etcd/etcd-2026-07-24_10-40-35.db -w table
```
#### Должны получить примерно 
```
+----------+----------+------------+------------+---------+
|   HASH   | REVISION | TOTAL KEYS | TOTAL SIZE | VERSION |
+----------+----------+------------+------------+---------+
| 93c1c664 |  2695668 |        950 |      60 MB |   3.6.0 |
+----------+----------+------------+------------+---------+
```

### Останавливаем все экземляры etcd
```
systemctl stop etcd
systemctl is-active etcd
```
Должно быть `inactive`

### Бэкапим основной etcd
```
mv /var/lib/etcd /var/lib/etcd.before-restore
```

### Востанавливаем на всех экземлярах etcd backup
etcd1
```
etcdutl snapshot restore \
  /var/backups/etcd/etcd-2026-07-24_10-40-35.db \
  --name=etcd1 \
  --data-dir=/var/lib/etcd \
  --initial-cluster="etcd1=https://192.168.1.1:2380,etcd2=https://192.168.1.2:2380,etcd3=https://192.168.1.3:2380" \
  --initial-cluster-token=k8s_etcd \
  --initial-advertise-peer-urls=https://192.168.1.1:2380 \
  --bump-revision=1000000000 \
  --mark-compacted
```
etcd2
```
etcdutl snapshot restore \
  /var/backups/etcd/etcd-2026-07-24_10-40-35.db \
  --name=etcd2 \
  --data-dir=/var/lib/etcd \
  --initial-cluster="etcd1=https://192.168.1.1:2380,etcd2=https://192.168.1.2:2380,etcd3=https://192.168.1.3:2380" \
  --initial-cluster-token=k8s_etcd \
  --initial-advertise-peer-urls=https://192.168.1.2:2380 \
  --bump-revision=1000000000 \
  --mark-compacted
```
etcd3
```
etcdutl snapshot restore \
  /var/backups/etcd/etcd-2026-07-24_10-40-35.db \
  --name=etcd2 \
  --data-dir=/var/lib/etcd \
  --initial-cluster="etcd1=https://192.168.1.1:2380,etcd2=https://192.168.1.2:2380,etcd3=https://192.168.1.3:2380" \
  --initial-cluster-token=k8s_etcd \
  --initial-advertise-peer-urls=https://192.168.1.2:2380 \
  --bump-revision=1000000000 \
  --mark-compacted
```

### Проверяем состояние кластера
```
etcdctl \
  --endpoints=https://192.168.1.1:2379,https://192.168.1.1:2379,https://192.168.1.3:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-$(hostname).pem \
  --key=/etc/ssl/etcd/ssl/member-$(hostname)-key.pem \
  endpoint health -w table
```
```
etcdctl \
  --endpoints=https://192.168.1.1:2379,https://192.168.1.2:2379,https://192.168.1.3:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-$(hostname).pem \
  --key=/etc/ssl/etcd/ssl/member-$(hostname)-key.pem \
  endpoint status -w table
```
```
etcdctl \
  --endpoints=https://127.0.0.1:2379 \
  --cacert=/etc/ssl/etcd/ssl/ca.pem \
  --cert=/etc/ssl/etcd/ssl/member-$(hostname).pem \
  --key=/etc/ssl/etcd/ssl/member-$(hostname)-key.pem \
  member list -w table
```
### Востановление окончено проверяйте приложения
