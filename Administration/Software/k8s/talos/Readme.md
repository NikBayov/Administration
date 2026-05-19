# Установка кластера k8s на talos OS
!https://docs.siderolabs.com/talos/v1.13/getting-started/quickstart
|       talos-mn1     |     talos-wn1     |     talos-wn2   |
|---------------------|-------------------|-----------------|
|    192.168.0.140    |   192.168.0.141   |  192.168.0.142  |

### Скачивает актуальный ISO  и устанавливаем его на виртуалки
```
https://github.com/siderolabs/talos
```
### После запуска нажимаем F3 и настраиваем сеть

### Устанавливаем talosctl(я на windows ставлю)
#### Скачиваем talosctl-windows-amd64.exe из github и переименовывыаем в talosctl.exe у меня путь `C:\Tools\talos\`
### После задём путь в powershell
```
[Environment]::SetEnvironmentVariable(
  "Path",
  $env:Path + ";C:\Tools\talos",
  [EnvironmentVariableTarget]::User
)
```
### Перезапускаем PS и проверяем
```
talosctl version --client
```

### После генерируем конфиги
```
mkdir C:\talos-lab
cd C:\talos-lab

talosctl gen config talos-lab https://192.168.1.140:6443 --output-dir .
```
### Появятся:
```
controlplane.yaml
worker.yaml
talosconfig
```
### Заходим в нужный нам конфиг и настраиваем(с коробки тоже работает) и применяем
```
talosctl apply-config `
  --insecure `
  --nodes 192.168.1.140 `
  --file .\controlplane.yaml
```
```
talosctl apply-config `
  --insecure `
  --nodes 192.168.1.141 `
  --file .\worker.yaml
```

### Настраиваем talosconfig 

```PowerShell
$env:TALOSCONFIG="$PWD\talosconfig"
```
```PowerShell
talosctl config endpoint 192.168.1.140 
talosctl config node 192.168.1.141
```

### Выполняем Bootstrap кластера
```
talosctl bootstrap --nodes 192.168.1.140
```
### Получаем kubeconfig
```
talosctl kubeconfig --nodes 192.168.1.140
```
### Проверяем кластер
```
kubectl get nodes
```
# Установка окончена
