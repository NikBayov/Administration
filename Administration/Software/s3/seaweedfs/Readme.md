# Установка seaweedfs для s3 хранилища на ВМ Debian13
!https://github.com/seaweedfs/seaweedfs#quick-start

### Подготавливаемся к установке 
```
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget unzip
```

### Скачиваем seaweedfs

```
wget https://github.com/seaweedfs/seaweedfs/releases/latest/download/linux_amd64.tar.gz
tar -xzf linux_amd64.tar.gz
sudo mv weed /usr/local/bin/
```

### Проверяем установку 

```
weed version
```
