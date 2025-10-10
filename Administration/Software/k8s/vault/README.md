# Установка vault в kubernetes

### Скачиваем Helm-chart с зеркала
```
helm pull oci://cr.yandex/yc-marketplace/yandex-cloud/vault/chart/vault \
  --version 0.28.1+yckms \
  --untar && cd vault
```
### Создаём namespace
```
kubectl create ns vault
```
### Редакдируем values.yaml под наши запросы(пример оставил в example-values.yaml)

### Устанавливаем чарт
```
helm upgrade --install vault . -n vault -f values.yaml
```
### Для настройки tls необходимо создать секрет с сертификатом(искать в др.гайдах)

### После заходим на страницу https://vault.example.ru и проходим процесс инициализации, !!!Все ключи сохраняем у себя

### После создания ключей, проходим процедуру распечатывания введя три ключа отдельно(я выбрал 5 ключей всего, и 3 чтоб распечатать)

### После распечатывания авторизуемся через корневой токен на прошлом шаге
