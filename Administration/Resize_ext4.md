### Отключаем swap и закоменти строку в /etc/fstab

```
$ swapoff -a
$ nano /etc/fstab
  #UUID=d8961527-8bbb-49db-af52-e77808bbcb4c none            swap    sw              0       0
```

### Запускаем cfdisk для расширения корневого раздела у нас /dev/sda1

```
$ cfdisk
```
### Удаляем все разделы кроме корневого

```
$ delete /dev/sda2
# Расширяем /dev/sda1
$ resize /dev/sda1
# Создаём заново /dev/sda2 с типом extended (Желатьльно 5Gb)
$ new /dev/sda2
# Сохраняем изменения
$ write/yes
```
### Применяем измениния на диск

```
$ resize2fs /dev/sda1
```

### Проверяем расширение диска

```
df -h
```
