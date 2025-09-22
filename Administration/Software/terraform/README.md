# Установка terraform на debian 12

### Скачиваем архив с `https://hashicorp-releases.yandexcloud.net/terraform/`
```
unzip terraform_1.13.2_linux_amd64.zip
```
### Устанавливаем terraform 
```
sudo mv terraform /usr/local/bin/
```
### Проверяем установку
```
usert@server:~# terraform version
Terraform v1.13.2
on linux_amd64
```
### В корневой папке пользователя создаём файл .terraformrc с содержимым:
```
provider_installation {
  network_mirror {
    url = "https://terraform-mirror.yandexcloud.net/"
    include = ["registry.terraform.io/*/*"]
  }
  direct {
    exclude = ["registry.terraform.io/*/*"]
  }
} 
```
# Установка завершена, можете использовать terraform и плагины для него
