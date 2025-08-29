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
  --disable traefik 
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
### Устанавливаем ingress
```
helm repo update
helm repo add ingress-nginx https://kubernetes.github.io/ingress-nginx
helm install ingress-nginx ingress-nginx/ingress-nginx   --namespace ingress-nginx   --create-namespace
```
