# Создаём pvc для тестового пода используя ceph

### Устанавливаем ceph-csi  с помощью helm 

```
helm repo add ceph-csi https://ceph.github.io/csi-charts
helm repo update
helm install ceph-csi-cephfs ceph-csi/ceph-csi-cephfs   --namespace cephfs   --create-namespace
```

### Проверяем что всё корректно запустилось

```
kubectl get pods -o wide -n cephfs
```
