### Выполняем обновление

```
sudo apt-get update -y
sudo apt-get install -y apt-transport-https ca-certificates curl gpg
```


### Устанавливаем Qemu

`sudo apt-get install qemu-system`

### Добавляем репозиторий kubectl

```
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.31/deb/Release.key | sudo gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg
echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.31/deb/ /' | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

### Устанавливаем  kubectl

```
sudo apt-get update -y
sudo apt install kubectl
```

### Устанавливаем minikube

```
curl -Lo minikube https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64   && chmod +x minikube
sudo mkdir -p /usr/local/bin/
sudo install minikube /usr/local/bin/
```

### Запускаем minikube(--forse это чтоб запускать от root)

`minikube start --driver=qemu --force`
