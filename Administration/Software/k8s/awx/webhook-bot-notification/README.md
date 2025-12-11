# Пример webhook для отправки уведомлений из awx 

### Необходимо в awx-deployment подставить значения в секрете `awx-base-url`,`bot-token`,`chat-id` и настроить ingress

```
kubectl apply -f awx-telegram-webhook.yaml
kubectl apply -f ingress-webohook.yaml
```

### После заходим в awx `Notifications->add` и настраиваем:

![screenshot](/cache/picture/awx-notice.jpg)
