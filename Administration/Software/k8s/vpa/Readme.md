# Установка VPA(Vertical Pod Autoscaler) в k8s 1.36  
!https://github.com/kubernetes/autoscaler.git

### Скачиваем VPA и устанавливаем
```
git clone https://github.com/kubernetes/autoscaler.git
cd autoscaler/vertical-pod-autoscaler

./hack/vpa-up.sh
```
### Проверяем установку 
```
kubectl get crd | grep verticalpodautoscalers
kubectl get pods -n kube-system | grep vpa
```
### Ожидаемо должны появиться такие компоненты:
```
vpa-recommender
vpa-updater
vpa-admission-controller
```
### Установка завершена для проверки можете создать 
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: vpa-test
  namespace: default
spec:
  replicas: 1
  selector:
    matchLabels:
      app: vpa-test
  template:
    metadata:
      labels:
        app: vpa-test
    spec:
      containers:
        - name: app
          image: registry.k8s.io/ubuntu-slim:0.1
          command:
            - /bin/sh
            - -c
            - |
              while true; do
                timeout 10s yes >/dev/null
                sleep 5
              done
          resources:
            requests:
              cpu: 10m
              memory: 32Mi
            limits:
              cpu: 50m
              memory: 64Mi
```

```
apiVersion: autoscaling.k8s.io/v1
kind: VerticalPodAutoscaler
metadata:
  name: vpa-test
  namespace: default
spec:
  targetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: vpa-test
  updatePolicy:
    updateMode: Auto
  resourcePolicy:
    containerPolicies:
      - containerName: app
        minAllowed:
          cpu: 10m
          memory: 32Mi
        maxAllowed:
          cpu: "1"
          memory: 512Mi
        controlledResources:
          - cpu
          - memory
```
### Применяем 
```
kubectl apply -f vpa-test-deploy.yaml
kubectl apply -f vpa-test-vpa.yaml
```
### Проверка рекомендаций
```
kubectl describe vpa vpa-test
```
Если там появились Target, Lower Bound, Upper Bound — рекомендации считаются.
Если pod пересоздался и resources стали другими — VPA отработал.
