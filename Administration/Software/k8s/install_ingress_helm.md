# Настройка ingress-nginx с помощью helm(на примере k8s-dashboard)

## Кластер k8s

|    k8s-mn1   |   k8s-wn1     |     k8s-wn2   |
|--------------|---------------|---------------|
| 192.168.0.70 | 192.168.0.71  | 192.168.0.72  |

### Создаём dashboard-ingress.yaml

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: kubernetes-dashboard-ingress
  namespace: kubernetes-dashboard
  annotations:
    nginx.ingress.kubernetes.io/backend-protocol: "HTTPS"
    nginx.ingress.kubernetes.io/secure-backends: "true"
    nginx.ingress.kubernetes.io/ssl-redirect: "true"
    nginx.ingress.kubernetes.io/ssl-passthrough: "true"
spec:
  ingressClassName: nginx
  rules:
  - host: dash-k8s.nikbayov.ru
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: kubernetes-dashboard
            port:
              number: 443
```

#### Запускаем 
```
kubectl apply -f dashboard-ingress.yaml
```

### Для dashboard небоходимо добавить параметр в `args` 

`- --enable-ssl-passthrough`

```
kubectl -n ingress-nginx edit deployment ingress-nginx-controller
```

### Yaml для dashboard 

```
apiVersion: v1
kind: Service
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Service","metadata":{"annotations":{},"labels":{"k8s-app":"kubernetes-dashboard"},"name":"kubernetes-dashboard","namespace":"kubernetes-dashboard"},"spec":{"ports":[{"port":443,"targetPort":8443}],"selector":{"k8s-app":"kubernetes-dashboard"}}}
  creationTimestamp: "2025-03-11T07:11:31Z"
  labels:
    k8s-app: kubernetes-dashboard
  name: kubernetes-dashboard
  namespace: kubernetes-dashboard
  resourceVersion: "390295"
  uid: 2a85dc82-4145-4e47-b034-c7f7832a9516
spec:
  clusterIP: 10.107.125.11
  clusterIPs:
  - 10.107.125.11
  internalTrafficPolicy: Cluster
  ipFamilies:
  - IPv4
  ipFamilyPolicy: SingleStack
  ports:
  - port: 443
    protocol: TCP
    targetPort: 8443
  selector:
    k8s-app: kubernetes-dashboard
  sessionAffinity: None
  type: ClusterIP
status:
  loadBalancer: {}
```
