# Установка k8s v.1.31 через kubeadm на Debian 12.7, 1  master node and 2 worker node

## Примечание: Все шаги со знаком `*` выполняются для всех node

## Подготовка сервера*

#### Отключаем swap*

```
sudo swapoff -a
nano /etc/fstab
#Коментируем строку со swap
```

### Меняем имя сервера*

`k8s-m`- Master node
`k8s-w1`- Worker node 1
`k8s-w2`- Worker node 2

```
sudo hostnamectl set-hostname k8s-m 
nano /etc/hosts

     127.0.0.1 localhost
     127.0.1.1 k8s-m

```
### Выполняем обновление*

```
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl gpg

```

### Добавляем репозиторий k8s*

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.32/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.32/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

### Устанавливаем  стек k8s* 

```
sudo apt-get update -y
sudo apt-get install -y kubelet kubeadm kubectl containerd
sudo apt-mark hold kubelet kubeadm kubectl
```

### Активируем необходимые модули*

```
modprobe br_netfilter
modprobe overlay
```

### Настраиваем сеть для общения внутри кластера*

```
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf
echo "net.bridge.bridge-nf-call-iptables=1" >> /etc/sysctl.conf # Если есть iptables
sysctl -p /etc/sysctl.conf
```

### Настраиваем containerd*

```
sudo mkdir /etc/containerd/
sudo nano /etc/containerd/config.toml
```
```
version = 2
[plugins]
  [plugins."io.containerd.grpc.v1.cri"]
   [plugins."io.containerd.grpc.v1.cri".containerd]
      [plugins."io.containerd.grpc.v1.cri".containerd.runtimes]
        [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc]
          runtime_type = "io.containerd.runc.v2"
          [plugins."io.containerd.grpc.v1.cri".containerd.runtimes.runc.options]
            SystemdCgroup = true
```
```
sudo systemctl restart containerd            
```
### Инициализируем кластер(k8s-m)
###### to access kubernetes from external network you need to additionaly set flag with external ip --apiserver-cert-extra-sans=158.160.111.211

```
sudo kubeadm init \
  --apiserver-advertise-address="ip-k8s-m" \
  --pod-network-cidr 10.244.0.0/16
```

### Делааем стандартную конфигурацию k8s

```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```

### Устанавливаем cni flannel

```
kubectl apply -f https://github.com/flannel-io/flannel/releases/latest/download/kube-flannel.yml
```

### Добавляем worker nodes(k8s-w1,k8s-w2)
#### Генерируем токен на k8s-m

``` 
kubeadm token generate
```

#### Вводим сгенерированный токен и получаем полную команду для добавления worker на k8s-m
```
kubeadm token create <generated-token> --print-join-command --ttl=0
```

### Вводим команду на k8s-w1,k8s-w2

```
sudo kubeadm join 10.128.0.28:6443 --token zvxm7y.z61zq4rzaq3rtipk \
        --discovery-token-ca-cert-hash sha256:9b650e50a7a5b6261746684d033a7d6483ea5b84db8932cb70563b35f91080f7
```        

### Команды которые могут пригодиться

#### Удалить узел из кластера
`kubectl delete node node-name`

#### Удалить существующие файлы конфигурации
```
sudo rm -f /etc/kubernetes/kubelet.conf
sudo rm -f /etc/kubernetes/pki/ca.crt
```

#### Очистка конфигурации узла
`kubeadm reset`

#### Проверка конфигурации кластера
`kubectl get nodes`

#### Посмотреть статус pods
`kubectl get pods --all-namespaces -o wide`

#### Посмотреть логи pod
`kubectl logs <pod-name> -n <namespace>`

#### Перезапустить pod
`kubectl delete pod <pod-name> -n <namespace>`

#### Посмотреть события кластера
`kubectl get events`

