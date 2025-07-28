# Установка опреатора AWX в кластер k8s

### Подготовим PV, я буду использовать свой кластер ceph(cephfs-sc)
```
root@k8s-mn1:~/deploy/awx-operator# kubectl get sc
NAME                  PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
cephfs-db             cephfs.csi.ceph.com   Retain          Immediate           false                  41d
cephfs-sc (default)   cephfs.csi.ceph.com   Retain          Immediate           true                   55d
csi-cephfs-sc         cephfs.csi.ceph.com   Delete          Immediate           true                   55d
```

### Установим необходимые пакеты, я ставлю на k8s-mn1
```
sudo apt update
sudo apt install git build-essential curl jq  -y
```

### Клонируем проект
```
git clone https://github.com/ansible/awx-operator.git
cd awx-operator/
```
### Создаём ns
```
export NAMESPACE=awx
kubectl create ns ${NAMESPACE}
```
#### (Опционально) Делаем ns awx ns по умолчанию
```
kubectl config set-context --current --namespace=$NAMESPACE 
```
### Переходим в ветку с последней версией
```
RELEASE_TAG=`curl -s https://api.github.com/repos/ansible/awx-operator/releases/latest | grep tag_name | cut -d '"' -f 4`
echo $RELEASE_TAG
git checkout $RELEASE_TAG
```
### Устанавливаем AWX operator в k8s
```bash
export NAMESPACE=awx
make deploy
```
### Создаём PVC для файлов 
```
cat <<EOF | kubectl create -f -
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: awx-static-data-pvc
  namespace: awx
spec:
  accessModes:
    - ReadWriteOnce
  storageClassName: cephfs-sc
  resources:
    requests:
      storage: 10Gi
EOF
```
###  Создаём deployment awx-deployment.yml
```
apiVersion: awx.ansible.com/v1beta1
kind: AWX
metadata:
  name: awx
spec:
  service_type: nodeport
  projects_persistence: true
  projects_storage_access_mode: ReadWriteOnce
  web_extra_volume_mounts: |
    - name: static-data
      mountPath: /var/lib/projects
  extra_volumes: |
    - name: static-data
      persistentVolumeClaim:
        claimName:  awx-static-data-pvc
```
### Проверяем поды
```
kubectl get pods -l "app.kubernetes.io/managed-by=awx-operator" -w
```
### Проверяем логи
```
kubectl -n awx  logs deploy/awx
```
#### Если нужен отдельный контейнер
```
kubectl -n awx  logs deploy/awx -c redis
kubectl -n awx  logs deploy/awx -c awx-web
kubectl -n awx  logs deploy/awx -c awx-task
kubectl -n awx  logs deploy/awx -c awx-ee
```
#### Если нужно подключиться к облочке
```
kubectl exec -ti deploy/awx  -c  awx-task -- /bin/bash
kubectl exec -ti deploy/awx  -c  awx-web -- /bin/bash
kubectl exec -ti deploy/awx  -c  awx-ee -- /bin/bash
kubectl exec -ti deploy/awx  -c  redis -- /bin/bash
```
