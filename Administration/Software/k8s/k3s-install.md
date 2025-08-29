# Установка k3s с calico и ingress-nginx
|       k3s-mn1      |      k3s-wn1      |      k3s-wn2    |
|--------------------|-------------------|-----------------|
|    192.168.0.75    |   192.168.0.76    |  192.168.0.77   |
### Подготавливаем ВМ
```
apt update
apt install curl wget net-tools sudo

```
```
sudo swapoff -a
nano /etc/fstab
#Коментируем строку со swap
```
```
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
echo "net.bridge.bridge-nf-call-iptables=1" >> /etc/sysctl.conf 
sysctl -p /etc/sysctl.conf
```

### Устанавливаем k3s на mn1 

```
curl -sfL https://get.k3s.io | sh -s - \
  --flannel-backend=none \
  --disable-network-policy \
  --disable local-storage \
  --disable traefik \
```
### Устанавливаем calico на mn1

```
kubectl create -f https://raw.githubusercontent.com/projectcalico/calico/v3.26.4/manifests/tigera-operator.yaml
```
### Настраиваем calico
```
nano custom-resources.yaml
```

```
apiVersion: operator.tigera.io/v1
kind: Installation
metadata:
  name: default
spec:
  calicoNetwork:
    ipPools:
    - blockSize: 26
      cidr: 10.42.0.0/16  # Должен совпадать с pod-сетью k3s (по умолчанию 10.42.0.0/16)
      encapsulation: VXLANCrossSubnet
      natOutgoing: Enabled
      nodeSelector: all()
---
apiVersion: operator.tigera.io/v1
kind: APIServer
metadata:
  name: default
spec: {}
```
```
kubectl apply -f custom-resources.yaml
```
### Проверяем что всё работает 
```
kubectl get pods -o wide --all-namespaces
```

### Удалёем traefik
```
kubectl delete -n kube-system deployment traefik
kubectl delete -n kube-system service traefik
kubectl delete clusterrole traefik
kubectl delete clusterrolebinding traefik
kubectl delete -n kube-system serviceaccount traefik
kubectl delete crd aiservices.hub.traefik.io
kubectl delete crd apiaccesses.hub.traefik.io
kubectl delete crd apibundles.hub.traefik.io
kubectl delete crd apicatalogitems.hub.traefik.io
kubectl delete crd apiplans.hub.traefik.io
kubectl delete crd apiportals.hub.traefik.io
kubectl delete crd apiratelimits.hub.traefik.io
kubectl delete crd apis.hub.traefik.io
kubectl delete crd apiversions.hub.traefik.io
kubectl delete crd ingressroutes.traefik.io
kubectl delete crd ingressroutetcps.traefik.io
kubectl delete crd ingressrouteudps.traefik.io
kubectl delete crd managedsubscriptions.hub.traefik.io
kubectl delete crd middlewares.traefik.io
kubectl delete crd middlewaretcps.traefik.io
kubectl delete crd serverstransports.traefik.io
kubectl delete crd serverstransporttcps.traefik.io
kubectl delete crd tlsoptions.traefik.io
kubectl delete crd tlsstores.traefik.io
kubectl delete crd traefikservices.traefik.io

```
```
kubectl delete pod -n kube-system helm-install-traefik-crd-x85rw
kubectl delete pod -n kube-system helm-install-traefik-kctkr
```
### Устанавливаем ingress
```
helm repo update
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx   --namespace ingress-nginx   --create-namespace
```
