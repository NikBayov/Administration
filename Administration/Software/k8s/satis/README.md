# Установка Satis-server в k8s на примере размещения репозитория composer v1.6 для php7.1

### Создаём satis.json и указываем в нём необходимые пакеты для загрузки
### Указываем имя  и домен нашего репо  и дальше пакеты
```
{
  "name": "nikbayov/satis-repo", 
  "homepage": "https://satis.nikbayov.ru",
  "repositories": [
    {
      "type": "composer",
      "url": "https://packagist.org"
    },
    {
      "type": "composer",
      "url": "https://asset-packagist.org"
    }	
```
### Далее добавляем содержимое satis.json в configmap.yaml

### Далее создаём DP для nginx пода, чтоб был доступ к веб-интерфейсу
### Также создаём cronjob,ingress,pvc,dockerfile,tls,service
```
kubectl apply -f ConfigMap.yaml -n satis
kubectl apply -f cronjob.yaml -n satis
kubectl apply -f ingress.yaml -n satis
kubectl apply -f pvc.yaml -n satis
kubectl apply -f tls.yaml -n satis
kubectl apply -f service.yaml -n satis
```
### Далее запустится cronjob и скачает все пакеты на pvc
##### я сделал cronjob мануально, чтобы перезапустить job
```
kubectl create job --from=cronjob/satis-build satis-manual-$(date +%s) -n satis
```
### Заходим на домен и проверяем, что локальный реп готов
