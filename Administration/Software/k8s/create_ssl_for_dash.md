# Выпуск ssl сертификата в k8s для любого домена на примере dash-k8s.nikbayov.ru

### Устанавливаем certmanager

```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.3/cert-manager.yaml
```

#### Ждём пару минут и проверяем его работу
```
kubectl get pods -n cert-manager
```

### Создаём cluster-issuer.yaml

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: letsencrypt-prod
spec:
  acme:
    email: niketxbox@gmail.com # <-- укажи свой реальный email
    server: https://acme-v02.api.letsencrypt.org/directory
    privateKeySecretRef:
      name: letsencrypt-prod
    solvers:
    - http01:
        ingress:
          class: nginx
```

#### Применяем
```
kubectl apply -f cluster-issuer.yaml

```

### Обновляем Ingress с аннотациями для HTTPS + сертификата `dashboard-ingress.yaml`

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
    cert-manager.io/cluster-issuer: "letsencrypt-prod"
    acme.cert-manager.io/http01-edit-in-place: "true"
spec:
  ingressClassName: nginx
  tls:
  - hosts:
    - dash-k8s.nikbayov.ru
    secretName: dashboard-tls
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

#### Применяем 

```
kubectl apply -f dashboard-ingress.yaml
```

### Создаём `dashboard-cert.yaml`

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: dashboard-tls
  namespace: kubernetes-dashboard
spec:
  secretName: dashboard-tls
  dnsNames:
  - dash-k8s.nikbayov.ru
  issuerRef:
    name: letsencrypt-prod
    kind: ClusterIssuer
  usages:
  - digital signature
  - key encipherment
```

#### Применяем

```
kubectl apply -f dashboard-cert.yaml
```

### Проверяем стату серта через 1 мин

```
kubectl -n kubernetes-dashboard describe certificate dashboard-tls
```

### Вывод должен бфть примерно такой

```
root@k8s-mn1:~/deploy# kubectl -n kubernetes-dashboard describe certificate dashboard-tls
Name:         dashboard-tls
Namespace:    kubernetes-dashboard
Labels:       <none>
Annotations:  <none>
API Version:  cert-manager.io/v1
Kind:         Certificate
Metadata:
  Creation Timestamp:  2025-05-23T13:31:59Z
  Generation:          1
  Resource Version:    441980
  UID:                 39c59a28-cc19-4ce3-9352-51d57a7c0d3d
Spec:
  Dns Names:
    dash-k8s.nikbayov.ru
  Issuer Ref:
    Kind:       ClusterIssuer
    Name:       letsencrypt-prod
  Secret Name:  dashboard-tls
  Usages:
    digital signature
    key encipherment
Status:
  Conditions:
    Last Transition Time:  2025-05-26T08:24:45Z
    Message:               Certificate is up to date and has not expired
    Observed Generation:   1
    Reason:                Ready
    Status:                True
    Type:                  Ready
  Not After:               2025-08-24T07:26:11Z
  Not Before:              2025-05-26T07:26:12Z
  Renewal Time:            2025-07-25T07:26:11Z
  Revision:                2
Events:
  Type    Reason     Age                From                                       Message
  ----    ------     ----               ----                                       -------
  Normal  Issuing    2d18h              cert-manager-certificates-trigger          Issuing certificate as Secret was previously issued by "Issuer.cert-manager.io/"
  Normal  Reused     2d18h              cert-manager-certificates-key-manager      Reusing private key stored in existing Secret resource "dashboard-tls"
  Normal  Requested  2d18h              cert-manager-certificates-request-manager  Created new CertificateRequest resource "dashboard-tls-1"
  Normal  Issuing    2d18h              cert-manager-certificates-issuing          The certificate has been successfully issued
  Normal  Issuing    35s                cert-manager-certificates-trigger          Issuing certificate as Secret does not exist
  Normal  Generated  35s                cert-manager-certificates-key-manager      Stored new private key in temporary Secret resource "dashboard-tls-6gb8x"
  Normal  Requested  29s (x2 over 35s)  cert-manager-certificates-request-manager  Created new CertificateRequest resource "dashboard-tls-2"
  Normal  Issuing    21s                cert-manager-certificates-issuing          The certificate has been successfully issued
```
