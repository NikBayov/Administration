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
