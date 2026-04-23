# Установка NFS-сервера для legasy и k3s (Debian13)

### Устанавливаем nfs на сервер
```
sudo apt update
sudo apt install -y nfs-kernel-server
```

### Создаём необходимые нам "шары", я разделил на 3 типа
```
sudo mkdir -p /srv/nfs/shared
sudo mkdir -p /srv/nfs/k8s
sudo mkdir -p /srv/nfs/backup
```

### Выдаём права
```
sudo chown -R nobody:nogroup /srv/nfs
sudo chmod -R 0775 /srv/nfs
```

### Вносим данные сервера и шар в `/etc/exports`

```
/srv/nfs/shared  192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
/srv/nfs/k8s     192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
/srv/nfs/backup  192.168.1.0/24(rw,sync,root_squash,no_subtree_check)
```

Моя подсеть 192.168.1.0/24
rw — запись разрешена
sync — безопаснее для данных
root_squash — root на клиенте не становится root на сервере

### Сохраняем,применяем и проверяем
```
sudo exportfs -rav
sudo systemctl enable --now nfs-server
sudo systemctl status nfs-server
```
### Должно получиться примерно так:
```
root@nfs1:~# sudo systemctl status nfs-server
* nfs-server.service - NFS server and services
     Loaded: loaded (/usr/lib/systemd/system/nfs-server.service; enabled; preset: enabled)
    Drop-In: /run/systemd/generator/nfs-server.service.d
             `-order-with-mounts.conf
     Active: active (exited) since Thu 2026-04-23 08:31:18 EET; 2min 17s ago
 Invocation: ea2b304eb50a4abbb0cb598e8a2fd2b8
       Docs: man:rpc.nfsd(8)
             man:exportfs(8)
   Main PID: 5418 (code=exited, status=0/SUCCESS)
   Mem peak: 1.7M
        CPU: 15ms

Apr 23 08:31:18 nfs1 systemd[1]: Starting nfs-server.service - NFS server and services...
Apr 23 08:31:18 nfs1 exportfs[5416]: exportfs: can't open /etc/exports for reading
Apr 23 08:31:18 nfs1 sh[5419]: nfsdctl: lockd configuration failure
Apr 23 08:31:18 nfs1 systemd[1]: Finished nfs-server.service - NFS server and services.
root@nfs1:~# sudo exportfs -v
/srv/nfs/shared
                192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,secure,root_squash,no_all_squash)
/srv/nfs/k8s    192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,secure,root_squash,no_all_squash)
/srv/nfs/backup
                192.168.1.0/24(sync,wdelay,hide,no_subtree_check,sec=sys,rw,secure,root_squash,no_all_squash)

```

### Для монтирования клиента на сервере:
```
sudo apt install -y nfs-common
showmount -e {{IP_NFS_Server}}
sudo mkdir -p /mnt/shared
sudo mount -t nfs4 {{IP_NFS_Server}}:/srv/nfs/shared /mnt/shared
```

### Можно добавить в fstab
```
{{IP_NFS_Server}}:/srv/nfs/shared  /mnt/shared  nfs4  defaults,_netdev  0  0
```

### Для добавления в k3s  скачиваем helm и настраиваем 
```
helm pull csi-driver-nfs/csi-driver-nfs --untar
```
```
cd csi-driver-nfs && helm install csi-driver-nfs csi-driver-nfs/csi-driver-nfs   --namespace kube-system -f ./values.yaml
```

### Можно создать тестовый pvc для проверки файлы приложил
