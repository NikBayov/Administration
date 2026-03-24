# Настройка деплоя app(php+nginx) через helm в k8s-кластер

### 1.Создаём отдельный namespace и ServiceAccount:
```
apiVersion: v1
kind: ServiceAccount
metadata:
  name: {{username}}
  namespace: {{namespace}}
```
```
kubectl apply -f serviceaccount.yaml
```
### 2.Создаём Role + RoleBinding
```
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: {{username}}
  namespace: {{namespace}}
rules:
  - apiGroups: [""]
    resources:
      - configmaps
      - secrets
      - services
      - serviceaccounts
      - pods
      - pods/log
      - persistentvolumeclaims
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

  - apiGroups: ["apps"]
    resources:
      - deployments
      - statefulsets
      - daemonsets
      - replicasets
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

  - apiGroups: ["batch"]
    resources:
      - jobs
      - cronjobs
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

  - apiGroups: ["networking.k8s.io"]
    resources:
      - ingresses
      - networkpolicies
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

  - apiGroups: ["autoscaling"]
    resources:
      - horizontalpodautoscalers
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]

  - apiGroups: ["policy"]
    resources:
      - poddisruptionbudgets
    verbs: ["get", "list", "watch", "create", "update", "patch", "delete"]
```

```
apiVersion: rbac.authorization.k8s.io/v1
kind: RoleBinding
metadata:
  name: {{username}}-binding
  namespace: {{namespace}}
subjects:
  - kind: ServiceAccount
    name: {{username}}
    namespace: {{namespace}}
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: Role
  name: {{username}}
```
```
kubectl apply -f role.yaml
kubectl apply -f rolebinding.yaml
```
### 3.Получаем токен ServiceAccount

```
kubectl -n {{namespace}} create token {{username}}
```
### 4.Собираем kubeconfig

```
apiVersion: v1
kind: Config
clusters:
- name: your-cluster
  cluster:
    server: https://YOUR-K8S-API:6443
    certificate-authority-data: YOUR_BASE64_CA_DATA

users:
- name: {{username}}
  user:
    token: YOUR_SERVICEACCOUNT_TOKEN

contexts:
- name: {{username}}@your-cluster
  context:
    cluster: your-cluster
    user: {{username}}
    namespace: {{namespace}}

current-context: {{username}}@your-cluster
```
