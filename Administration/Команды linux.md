`ip a` -узнать свой ip

`cd` -обратится к директории

`pwd` -где мы 

`mkdir` -создать директорию

`sudo rm -rf(-f)` -удалить файл

`cp` -копировать 

`cat(/proc/...)` -узнать информацию о системе

`man `"командна"- узнать все свойтсва команды

`useradd`(создать пол -m(создание папки) -s(доступ к облочке) /bin/bash "имя п"

`sudo usermod -aG` "группа к примеру "sudo"" "пол"

`mv` -вырезать

`sudo systemctl status` "ssh"-проверка проги

`tail -f /var/log/syslog` -просмотр лога

`iptables -I INPUT -p tcp --dport 10000 -m state --state NEW -j ACCEPT`  -открытие порта 10000

`grep "$DATE" /var/log/nginx/*access.log | awk '{print $1}' | sort | uniq -c | sort -nr | head -n 10` -проверка сколько подключений к сайту

`atop -r /var/log/atop/atop_20231204 -b 202312141655 -c`  -просмотр логов

`du -hc --max-depth=1 /home/bitrix/www/upload/` -проверить скоколько занимают папки внутри указанной папки(шаг 1)

`sudo tar -zcvf namefile.tar.gz --exclude=/tmp --exclude=/dev  --exclude=/proc /` - Создание архива

`chmod --reference=`(Файл с правами) (файл без прав)   -можно указать несколько файлов

////Синтаксис для клонирования владельца другого файла или каталога на Linux

`chown --reference=` (Файл с правами) (файл без прав) 

////при копировании cp

-p - сохранять владельца, временные метки и флаги доступа при копирование

cp (файл копирования) (место копирования)
