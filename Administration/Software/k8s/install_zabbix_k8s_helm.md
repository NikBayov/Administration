# Установка Zabbix сервер в кластере k8s через Helm

### Добавляем репозиторий zabbix

```
helm repo add zabbix-community https://zabbix-community.github.io/helm-zabbix
helm repo update
```

### Выбираем нужную нам версию

```
helm search repo zabbix-community/zabbix -l
```
#### Закрепляем версию
```
export ZABBIX_CHART_VERSION='7.0.8'
```

### Скачиваем архив

```
helm pull zabbix-community/zabbix
```

### Распаковываем архив 

```
tar -zxvf zabbix-7.0.8.tgz
```

### Редактируем файл `values.yaml`
`Файл слишком большой, поэтому просто приложу его по пути /k8s/zabbix`

### Создаём zabbix

```
helm upgrade --install zabbix zabbix-community/zabbix --values /root/deploy/zabbix/zabbix/values.yaml -n monitoring
```

### Проверяем 
```
kubectl get pods -n monitoring
```
