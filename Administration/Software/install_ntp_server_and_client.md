# Установка NTP-сервера(Chrony)

### Подготовка к установке

`Открыть 123 порт`

### Устанавливаем chrony

```
sudo apt update
sudo apt install chrony
```

### Настраиваем конфигурационный файл /etc/chrony/chrony.conf

`nano /etc/chrony/chrony.conf`

### Итоговая конфигурация должна выглядеть так:

```
# Welcome to the chrony configuration file. See chrony.conf(5) for more
# information about usable directives.

# Include configuration files found in /etc/chrony/conf.d.
confdir /etc/chrony/conf.d

# Use Debian vendor zone.
pool 2.debian.pool.ntp.org iburst # Пул с которым синхронизируется время
# Use time sources from DHCP.
sourcedir /run/chrony-dhcp

# Use NTP sources found in /etc/chrony/sources.d.
sourcedir /etc/chrony/sources.d

# This directive specify the location of the file containing ID/key pairs for
# NTP authentication.
keyfile /etc/chrony/chrony.keys

# This directive specify the file into which chronyd will store the rate
# information.
driftfile /var/lib/chrony/chrony.drift

# Save NTS keys and cookies.
ntsdumpdir /var/lib/chrony

# Uncomment the following line to turn logging on.
log tracking measurements statistics

# Log files location.
logdir /var/log/chrony

# Stop bad estimates upsetting machine clock.
maxupdateskew 100.0

# This directive enables kernel synchronisation (every 11 minutes) of the
# real-time clock. Note that it can't be used along with the 'rtcfile' directive.
rtcsync

# Step the system clock instead of slewing it if the adjustment is larger than
# one second, but only in the first three clock updates.
makestep 1 3
manual
local stratum 8
# Get TAI-UTC offset and leap seconds from the system tz database.
# This directive must be commented out when using time sources serving
# leap-smeared time.
leapsectz right/UTC
allow 172.17.0.0/16 
allow 10.0.0.0/8
```

#### Примечание: обязательно в конфигурации необходимо разрешить доступ к серверу из ЛВС добавив строки в nano /etc/chrony/chrony.conf

```
allow 172.17.0.0/16 
allow 10.0.0.0/8
```

#### Также в качестве pool и server для синхронизации можно использовать любые публичные ntp-севера
#### К примеру:

```
server 0.ru.pool.ntp.org iburst
server 1.ru.pool.ntp.org iburst
server 2.ru.pool.ntp.org iburst
server 3.ru.pool.ntp.org iburst
```
#### Параметр `iburst` задаёт приоритет с какого сервера синхронизировать время

### Перезапускаем chrony

`systemctl restart chrony`

### Проверяем что служба работает корректно

`systemctl status chrony`

### Проверяем что время синхронизировано

`timedatectl`

##### Должно быть примерно так

```
root@chrony:~# timedatectl
               Local time: Fri 2024-12-06 09:15:45 MSK
           Universal time: Fri 2024-12-06 06:15:45 UTC
                 RTC time: Fri 2024-12-06 06:15:45
                Time zone: Europe/Moscow (MSK, +0300)
System clock synchronized: yes
              NTP service: active
          RTC in local TZ: no
```

# Настройка клиента для подключения к нашему ntp-серверу

### Устанавливаем chrony

```
sudo apt update
sudo apt install chrony
```

### Редактируем конфигурационный файл /etc/chrony/chrony.conf

```
confdir /etc/chrony/conf.d
server <ip.local.ntp.server> iburst
sourcedir /run/chrony-dhcp
sourcedir /etc/chrony/sources.d
keyfile /etc/chrony/chrony.keys
driftfile /var/lib/chrony/chrony.drift
ntsdumpdir /var/lib/chrony
log tracking measurements statistics
logdir /var/log/chrony
maxupdateskew 100.0
rtcsync
makestep 1 3
leapsectz right/UTC
```

### Проверяем синхронизацию с сервером

`systemctl status chrony`

`timedatectl`

##### Должны быть строки

```
Dec 06 01:23:07 client-chrony chronyd[903]: Selected source <ip.local.ntp.server>
Dec 06 01:23:07 client-chrony chronyd[903]: System clock TAI offset set to 37 seconds
```


# Синхронизация с помощью стандартной timesyncd

### Редактируем конфигурационный файл /etc/systemd/timesyncd.conf

`echo "NTP=<ip.addr.ntp.server>" >> /etc/systemd/timesyncd.conf`

### Проверка

`timedatectl`

# Полезные команды

#### Проверить подключенных клиентов к серверу

`chronyc clients`

##### В выводе:

`Hostname` — имя или адрес клиента;
`NTP` — количество NTP-пакетов, полученных от клиентов;
`Drop` — сколько NTP-пакетов было отброшено из-за ограничения скорости отклика;
`Int` — средний интервал между NTP-пакетами;
`Last` — время с момента получения последнего NTP-пакета;


#### Показывает статистику всех серверов с которыми синхронизировано время

`chronyc activity`

#### Мгновенно синхронизировать время

`chronyc makestep`

#####  Мотивация: немедленная синхронизация системных часов может быть полезна в ситуациях, когда вам нужно быстро синхронизировать системные часы с более точным эталоном или исправить значительное отклонение во времени. Эта команда позволяет обойти постепенную настройку (переход), которая обычно выполняется демоном Chrony.

#### Проверка синхронизации

`chronyc tracking`

#### Перечисленные пункты содержат следующую информацию:

`Reference ID` — идентификатор и имя, с которым компьютер в настоящее время синхронизирован.
`Stratum` — количество переходов к компьютеру с установленными основными часами.
`Ref time` — это время по Гринвичу, в которое было выполнено последнее измерение из эталонного источника.
`System time` — задержка системных часов от синхронизированного сервера.
`Last offset` — расчетное смещение последнего обновления часов.
`RMS offset` — долгосрочное среднее арифметическое значения смещения.
`Frequency` — это частота, на которой часы системы будут работать неправильно, если хронограф не проведет коррекцию. Она выражена в ppm — ч/м (частей на миллион).
`Residual freq` — остаточная частота указывает на разницу между измерениями от опорного источника и используемой в настоящее время частотой.
`Skew` — расчетная погрешность, связанная с погрешностью частоты.
`Root delay` — суммарная задержка сетевого пути к опорному серверу, с которым синхронизируется компьютер.
`Leap status` — это статус, который может иметь одно из следующих значений — нормальное, добавить второй, удалить второй или не синхронизироваться.

#### Проверка связи с ntp-серверами

`chronyc sources -v`

##### где:

`poll` — периодичность синхронизации с этим сервером;
`reach` — состояние работоспособности. Если удалось произвести синхронизации восемь раз в подряд становится равным 377;
`*` — с этим сервером синхронизирует время наш ntpd;
`+` — сервер можно использовать для сверки часов;
`-` — не рекомендован для синхронизации;
`x`— не доступен.

#### Отображение подробной информации о каждом источнике NTP
`chronyc ntpdata`
