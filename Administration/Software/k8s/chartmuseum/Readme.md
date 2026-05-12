# Установка локально helm-репозитория в k8s 

### Скачиваем helm-chrat для chartmuseum/chartmuseum
```
helm repo add chartmuseum https://chartmuseum.github.io/charts
helm repo update
helm pull chartmuseum/chartmuseum --untar
```
### Настраиваем values.yaml и создаём сертификат tls для ingress если нужно и устанавливаем
```
helm upgrade chartmuseum chartmuseum/chartmuseum --install --create-namespace -n chartmuseum -f values.yaml
```
