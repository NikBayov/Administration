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

### Создаём всё

```
kubectl apply -f csi-cephfs-secret.yaml -n cephfs
kubectl apply -f Storageclass.yaml -n cephfs
kubectl apply -f ceph-configmap.yaml -n cephfs
```

### Создаём pvc.yaml для теста

```
apiVersion: v1
kind: PersistentVolume
metadata:
  name: test-app
spec:
  capacity:
    storage: 1Gi
  accessModes:
    - ReadWriteMany
  persistentVolumeReclaimPolicy: Retain
  storageClassName: cephfs-sc
  csi:
    driver: cephfs.csi.ceph.com
    volumeHandle: test-app
    volumeAttributes:
      clusterID: 7be0067a-146d-11f0-b650-bc24118cd3de
      fsName: cephfs
      pool: kube_data
    nodeStageSecretRef:
      name: csi-cephfs-secret
      namespace: cephfs
    controllerExpandSecretRef:
      name: csi-cephfs-secret
      namespace: cephfs
    controllerPublishSecretRef:
      name: csi-cephfs-secret
      namespace: cephfs
    nodePublishSecretRef:
      name: csi-cephfs-secret
      namespace: cephfs

```

```
kubectl apply -f pv.yaml
```

### Создаём pvc.yaml для тестовго пода

```
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: test-app
spec:
  accessModes:
    - ReadWriteMany
  resources:
    requests:
      storage: 1Gi
  volumeMode: Filesystem
  storageClassName: cephfs-sc
```

```
kubectl apply -f pvc.yaml -n cephfs
```

### Создаём тестовый под tpod.yaml

```
apiVersion: v1
kind: Pod
metadata:
  name: csi-cephfs-demo-pod
spec:
  containers:
    - name: web-server
      image: docker.io/library/nginx:latest
      volumeMounts:
        - name: mypvc
          mountPath: /var/lib/www
  volumes:
    - name: mypvc
      persistentVolumeClaim:
        claimName: test-app
        readOnly: false
```

### Проверяем что всё работает

```
kubectl get pods -o wide -n cephfs
```

### Если всё запустилось
`тогда заходим в под создаём файл в /var/lib/www и проверяем появился ли он , с ВМ на которой примонтирован ceph`
