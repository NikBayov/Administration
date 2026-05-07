# Установка flux для управления кластером k8s
!Documentation https://fluxcd.io/flux/

### Устанавливаем flux-cli 
```
curl -s https://fluxcd.io/install.sh | sudo bash
```

### Создаём репозиторий с примерно такой струкутрой
```
flux-repo/
├── clusters/
│   ├── dev/
│   │   ├── flux-system/
│   │   ├── infrastructure.yaml
│   │   ├── apps/
│   │   └── kustomization.yaml
│   │
│   └── prod/
│       ├── flux-system/
│       ├── infrastructure.yaml
│       ├── apps/
│       └── kustomization.yaml
│
├── infrastructure/
│   ├── ingress-nginx/
│   ├── cert-manager/
│   ├── harbor/
│   └── monitoring/
│
└── apps/
    ├── satis/
    │   ├── helmrelease.yaml
    │   └── gitrepository.yaml
    │
    ├── redis/
    └── postgres/
```
### После клонируем репозиторий на вм с flux

```
git clone url.git
```
### Делаем первый запуск(у меня гитлаб) остальное смотрите в доке
```
flux bootstrap gitlab \
  --hostname=gitlab.com \
  --owner=your-group \
  --repository=your-project \
  --branch=main \
  --path=clusters/dev \
  --token-auth \
  --components-extra=image-reflector-controller,image-automation-controller \
  --personal
```
`{url gitlab.com/your-group/your-project.git}`
### Можем тестировать синхронизацию,тестовый проект можно из доки взять

### Чтоб не было проблем с доступом создаём секрет 
```
flux create secret git project-auth \
  --url=https://gitlab.com/your-group/your-project.git \
  --username= {USER} \
  --password={TOKEN-GITLAB-PAT}\
  --namespace={FLUX-NAMESPACE}
```
### и добавляем в gitrepository.yaml
```
spec:
  secretRef:
    name: project-auth
```

### Для проверки kustomization
```
flux get kustomizations -A
```
### Для проверки синхронизации git
```
flux get sources git -A
```
### Для проверки синхронизации helm
```
flux get helm -A
```

### Для проверки синхронизации ImageRepository
```
flux get image repository -A
```

### Проверяем какой тег flux выбрал(ImagePolicy)
```
flux get image policy -A
```

### Проверяем сделал ли Flux commit в Git(ImageUpdateAutomation)
```
flux get image update -A
```

###
```
```

###
```
```

###
```
```

###
```
```

