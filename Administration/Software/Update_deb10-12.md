##  Подготовка к обновлению
### Проверка версии debian

```
$ cat /etc/debian_version
```

### Чтобы обновить дистрибутив Debian, а заодно привести пакеты в порядок, выполните команды:

```
$ sudo apt update

$ sudo apt dist-upgrade

$ sudo apt --fix-broken install

$ sudo apt autoremove
```

### Заменяем репозитории

```
$ sudo nano /etc/apt/sources.list
```
#### Для Debian 11
```
deb https://deb.debian.org/debian bullseye main
deb-src https://deb.debian.org/debian bullseye main

deb https://deb.debian.org/debian bullseye-updates main
deb-src https://deb.debian.org/debian bullseye-updates main

deb http://security.debian.org/ bullseye-security main
deb-src http://security.debian.org/ bullseye-security main
```

#### Для Debian 12
```
deb https://deb.debian.org/debian bookworm main
deb-src https://deb.debian.org/debian bookworm main

deb https://deb.debian.org/debian bookworm-updates main
deb-src https://deb.debian.org/debian bookworm-updates main

deb http://security.debian.org/ bookworm-security main
deb-src http://security.debian.org/ bookworm-security main
```

### Обновляем репозитории

```
$ sudo apt update
```

### Обновляем минимально после замены каждого из репозитория

```
$ sudo apt upgrade --without-new-pkgs
```

### Обновление завершено
