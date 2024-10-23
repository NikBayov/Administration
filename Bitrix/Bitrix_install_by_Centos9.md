#Установка Bitix24(bitrix-vm)

## При установке ОС необходимо
```
1. Выбрать редакцию  "Server";
2. Инициализировать диск выбрав его и нажав "Done";
3. Задать пароль для root;
4. Выбрать timezone.
В конце установки нажать "Reboot now"
```
## После установки ОС ввести:

```
$ dnf clean all && dnf update -y
```
```
$ wget http://repo.bitrix.info/dnf/bitrix-env-9.sh && chmod +x bitrix-env-9.sh && ./bitrix-env-9.sh
```

### Предложет выключить SeLinux вводим 'y' и после перезагружаем

``` 
$ reboot -h now
```
```
$ ./bitrix-env-9.sh -s -p -H default -P -M 'Ie8HH2_8HO'
```
### Загружаем файл bitrixsetup.php в /home/bitrix/www и выдаём права

```
$ chown -R bitrix:bitrix /home/bitrix/www
```
### После открываем Web-страницу http://your.ip.address/bitrixsetup.php  и настраиваем
