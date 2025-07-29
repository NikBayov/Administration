# Установка опреатора AWX в кластер k8s

### Подготовим PV, я буду использовать свой кластер ceph(cephfs-sc)
```bash
root@k8s-mn1:~/deploy/awx-operator# kubectl get sc
NAME                  PROVISIONER           RECLAIMPOLICY   VOLUMEBINDINGMODE   ALLOWVOLUMEEXPANSION   AGE
cephfs-db             cephfs.csi.ceph.com   Retain          Immediate           false                  41d
cephfs-sc (default)   cephfs.csi.ceph.com   Retain          Immediate           true                   55d
csi-cephfs-sc         cephfs.csi.ceph.com   Delete          Immediate           true                   55d
```

### Установим необходимые пакеты, я ставлю на k8s-mn1
```bash
sudo apt update
sudo apt install git build-essential curl jq  -y
```

### Клонируем проект
```bash
git clone https://github.com/ansible/awx-operator.git
cd awx-operator/
```
### Создаём ns
```bash
export NAMESPACE=awx
kubectl create ns ${NAMESPACE}
```
#### (Опционально) Делаем ns awx ns по умолчанию
```bash
kubectl config set-context --current --namespace=$NAMESPACE 
```
### Переходим в ветку с последней версией
```bash
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
```bash
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
```bash
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
```bash
kubectl get pods -l "app.kubernetes.io/managed-by=awx-operator" -w
```
### Если есть ощибка `mkdir: cannot create directory '/var/lib/pgsql/data/userdata': Permission denied`

`Необходимо выдать права в pvc на корневую папку рекусивно`
```
chown 26:root /mnt/ceph/volumes/csi/csi-vol-29685f1b-4046-43a2-8cf8-65ee1c1d74c4
```

### Проверяем логи
```bash
kubectl -n awx  logs deploy/awx
```
#### Если нужен отдельный контейнер
```bash
kubectl -n awx  logs deploy/awx -c redis
kubectl -n awx  logs deploy/awx -c awx-web
kubectl -n awx  logs deploy/awx -c awx-task
kubectl -n awx  logs deploy/awx -c awx-ee
```
#### Если нужно подключиться к облочке
```bash
kubectl exec -ti deploy/awx  -c  awx-task -- /bin/bash
kubectl exec -ti deploy/awx  -c  awx-web -- /bin/bash
kubectl exec -ti deploy/awx  -c  awx-ee -- /bin/bash
kubectl exec -ti deploy/awx  -c  redis -- /bin/bash
```

### Заходим в веб-интерфейс http://ip_master:32628
```bash
root@k8s-mn1:~/deploy/awx-operator#  kubectl get svc
NAME                                              TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)        AGE
awx-operator-controller-manager-metrics-service   ClusterIP   10.100.110.105   <none>        8443/TCP       93m
awx-postgres-15                                   ClusterIP   None             <none>        5432/TCP       89m
awx-service                                       NodePort    10.109.184.112   <none>        80:32628/TCP   77m
```
### Пароль от admin узнаём:
```
kubectl get secret awx-admin-password -o go-template='{{range $k,$v := .data}}{{printf "%s: " $k}}{{if not $v}}{{$v}}{{else}}{{$v | base64decode}}{{end}}{{"\n"}}{{end}}'
```
### AWX Установлен
