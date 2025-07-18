# Полезные команды для k8s

### Удалить namespace
```
kubectl delete namespace <namespace_name>
```
### Добавить метку
```
kubectl label pods POD_NAME version=v1
```
### Узнать кол-во реплик
```
kubectl get rs
```
### Проверить текущий namespace по умолчанию
```
kubectl config view --minify | grep namespace
```
### Сменить namespace по умолчанию на default
```
kubectl config set-context --current --namespace=default
```
### Смотреть логи в режиме RT
```
kubectl logs deployments/configmap-volume --follow
```
### Проброс порта
```
kubectl port-forward service/configmap-sidecar-service 8081:8081 &
```
###
```
kubectl patch svc ingress-nginx-controller -n ingress-nginx \
  -p '{"spec": {"externalIPs": ["172.17.29.31"]}}'
```
### Посмотреть деплои в namespace cephfs
```
kubectl get deploy -n cephfs
```
### Изменить деплой ceph-csi-cephfs-provisioner
```
kubectl edit deploy -n cephfs ceph-csi-cephfs-provisioner
```
### Посмотреть ingress в namespace monitoring 
```
kubectl get ingress -n monitoring
```
### Задание роли(worker) node(k8s-wn3)
```
kubectl label node k8s-wn3 node-role.kubernetes.io/worker=worker
```
### Узнать каие поды запущены на ноде(k8s-mn1)
```
kubectl get pods --all-namespaces -o wide --field-selector spec.nodeName=k8s-mn1
```
### Чтоб разрешить запуск только на worker
```
spec:
  template:
    spec:
      affinity:
        nodeAffinity:
          requiredDuringSchedulingIgnoredDuringExecution:
            nodeSelectorTerms:
            - matchExpressions:
              - key: node-role.kubernetes.io/worker
                operator: Exists
      tolerations: 
        - key: node-role.kubernetes.io/worker
          operator: Exists
```
### Запретить создание новых подов на k8s-mn1
```
kubectl cordon k8s-mn1
```
### Перезаписать текущую конфигурацию
```
kubectl replace -f nginx.yaml
```
### 
```
```
###
```
```
### 
```
```
###
```
```
### 
```
```
###
```
```
### 
```
```
###
```
```
### 
```
```
###
```
```
### 
```
```
###
```
```
