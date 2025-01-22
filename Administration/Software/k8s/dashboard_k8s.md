# Установка Dashboard для k8s с помощью nodePort
### Устанавливаем Dashboard

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.7.0/aio/deploy/recommended.yaml
```
#### Проверяем что все развернулось корректно
```
kubectl get all -n kubernetes-dashboard
```
#### Меняем текстовый редактор 
```
export EDITOR=nano
source ~/.bashrc
```
### Редактируем конфиг 

`kubectl edit service/kubernetes-dashboard -n kubernetes-dashboard`
```
# Please edit the object below. Lines beginning with a '#' will be ignored,
# and an empty file will abort the edit. If an error occurs while saving this file will be
# reopened with the relevant failures.
#
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard">
  creationTimestamp: "2025-01-22T09:41:05Z"
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
  resourceVersion: "7191"
  uid: 7806c604-3fd0-48e1-9efd-714a63af66cb
spec:
  clusterIP: 10.108.83.111
  clusterIPs:
  - 10.108.83.111
  externalTrafficPolicy: Cluster
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - nodePort: 32321
    port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: NodePort
status:
  loadBalancer: {}
```

#### Проверяем поды
```
kubectl get all -n kubernetes-dashboard
```
#### После наш дашборд должен был запуститься по ссылке https://ip-master-node:32321

### Далее создаём токен
`nano k8s-serviceaccount.yml`
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: dashboard-admin
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: cluster-admin-rolebinding
subjects:
- kind: ServiceAccount
  name: dashboard-admin
  namespace: kubernetes-dashboard
  apiGroup: ""
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
```
#### Проверяем создание УЗ
`kubectl get sa -n kubernetes-dashboard`

### Также создаём dashboard-admin-token.yml
`nano dashboard-admin-token.yml`
```
apiVersion: v1
kind: Secret
metadata:
     name: dashboard-admin-token
     namespace: kubernetes-dashboard
     annotations:
        kubernetes.io/service-account.name: dashboard-admin
type: kubernetes.io/service-account-token
```

### Запускаем все конфиги
```
kubectl create -f k8s-serviceaccount.yml
kubectl apply -f dashboard-admin-token.yml
```

### Получаем токен
```
kubectl describe secret dashboard-admin-token -n kubernetes-dashboard
```
