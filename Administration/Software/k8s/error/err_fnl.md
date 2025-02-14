### 1. Загрузите модуль br_netfilter
```
modprobe br_netfilter
```

### 2. Добавьте параметры в /etc/sysctl.conf
```
nano /etc/sysctl.conf
```
#### Добавьте в конец:
```
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1
```

### Затем примените изменения:
```
sysctl --system
```
### 3. Создайте systemd-сервис для автоматической настройки
```
nano /etc/systemd/system/k8s-sysctl.service
```
#### Вставьте следующее:
```
[Unit]
Description=Apply sysctl parameters for Kubernetes
Before=kubelet.service

[Service]
Type=oneshot
ExecStart=/sbin/sysctl --system

[Install]
WantedBy=multi-user.target
```

### Затем включите и запустите сервис:
```
systemctl daemon-reload
systemctl enable k8s-sysctl
systemctl start k8s-sysctl
```

### 4. Перезапустите kubelet и Flannel
```
systemctl restart kubelet
kubectl delete pod -n kube-flannel --all
```
```
kubectl get pods -n kube-flannel
```
