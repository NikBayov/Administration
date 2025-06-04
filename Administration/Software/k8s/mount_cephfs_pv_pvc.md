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

## Создаём Secret с ключом доступа

### adminKey и userKey получаем с помощью команды 

```
ceph auth get client.admin
```

#### `csi-cephfs-secret.yaml`
```
apiVersion: v1
kind: Secret
metadata:
  name: csi-cephfs-secret
  namespace: cephfs
stringData:
  userID: admin
  userKey: AQD3CfVn4WK5MhAARMP8oFxvu93bp6a1+gw==

  adminID: admin
  adminKey: AQD3CfVn4WK5MhAAe2GoFxvu93bp6a1+gw==
```

### Создаём Storageclass.yaml

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: cephfs-sc
provisioner: cephfs.csi.ceph.com
parameters:
  clusterID: 7be0067a-146d-11f0-b650-bc24118cd3de
  fsName: cephfs
  pool: kube_data
  csi.storage.k8s.io/provisioner-secret-name: csi-cephfs-secret
  csi.storage.k8s.io/provisioner-secret-namespace: cephfs
  csi.storage.k8s.io/node-stage-secret-name: csi-cephfs-secret
  csi.storage.k8s.io/node-stage-secret-namespace: cephfs
reclaimPolicy: Retain
volumeBindingMode: Immediate
```

### Создаём ceph-configmap.yaml

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: ceph-csi-config
  namespace: cephfs
data:
  config.json: |-
    [
      {
        "clusterID": "7be0067a-146d-11f0-b650-bc24118cd3de",
        "monitors": [
          "ceph1_ip:6789",
          "ceph2_ip:6789",
          "ceph3_ip:6789"
        ]
      }
    ]

```
