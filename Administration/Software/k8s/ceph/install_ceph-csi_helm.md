# Добавления динамического создания pvc для k3s 

### Скачиваем chart и редактируем values.yaml
```
helm repo add ceph-csi https://ceph.github.io/csi-charts
helm repo update
helm pull ceph-csi/ceph-csi-cephfs --untar
```

### Ключевые параметры которые необходимо запомнить
```
csiConfig:
  - clusterID: $CEPH_CLUSTER_ID
    monitors: [$CEPH_MONITORS]
    readAffinity:
      enabled: true
      crushLocationLabels:
        - topology.kubernetes.io/region
        - topology.kubernetes.io/zone
storageClass:
  create: true
  name: cephfs-nvme
  clusterID: $CEPH_CLUSTER_ID
  fsName: $CEPHFS_FS
  pool: $CEPHFS_POOL

secret:
  create: true
  adminID: $CEPHFS_USERNAME
  adminKey: $CEPHFS_KEY
```
### Устанавливаем
```
helm install ceph-csi-cephfs ceph-csi/ceph-csi-cephfs   --namespace cephfs   --create-namespace -f values.yaml
```
