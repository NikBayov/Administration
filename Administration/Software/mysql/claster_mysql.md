# Создание Master-slave кластера mysql 10.11
## Настраиваем master сервер

#### Прописываем след. значения
```
sudo nano /etc/mysql/mysql.conf.d/mysqld.cnf 
```
```
server-id           = 1
log_bin             = /var/log/mysql/mysql-bin.log 
binlog_do_db        = mydb 
relay-log           = /var/log/mysql/mysql-relay-bin.log
bind-address        = 0.0.0.0
```
#### Перезапускаем mysql
```
systemctl restart mysql
```
#### Создаём пользователя для репликации
```
CREATE USER 'replica_user'@'replica_server_ip' IDENTIFIED BY 'password';
```
#### Выдаём права
```
GRANT REPLICATION SLAVE ON *.* TO 'replica_user'@'replica_server_ip';
FLUSH PRIVILEGES;
```
#### Создаём дамп бд в новом окне терминала
```
sudo mysqldump -u root mydb > mydb.sql
```
#### Разблокируем таблицы 
```
UNLOCK TABLES;
```
#### Копируем дамп на реплику 
```
scp mydb.sql username@replica_server_ip:/tmp/
```

## Настройка Slave

### Создаём исходную бд
```
CREATE DATABASE mydb;
```
### Импортируем дамп 
```
sudo mysql mydb < /tmp/mydb.sql
```
### Настраиваем конфиг mysql
`/etc/mysql/mysql.conf.d/mysqld.cnf `
```
server-id           = 2
log_bin             = /var/log/mysql/mysql-bin.log 
binlog_do_db        = wfm 
relay-log           = /var/log/mysql/mysql-relay-bin.log
bind-address            = 0.0.0.0
```
### Перезапускаем mysql 
```
sudo systemctl restart mysql
```
### Настраиваем репликацию 
#### MASTER_LOG_FILE и MASTER_LOG_POS получаем командой на мастере  SHOW MASTER STATUS;
```
MariaDB [(none)]> SHOW MASTER STATUS;
+------------------+----------+--------------+------------------+
| File             | Position | Binlog_Do_DB | Binlog_Ignore_DB |
+------------------+----------+--------------+------------------+
| mysql-bin.000084 |      775 | mydb          |                  |
+------------------+----------+--------------+------------------+
```
```
     CHANGE MASTER TO
     MASTER_HOST='MASTER_IP',
     MASTER_USER='replica_user',
     MASTER_PASSWORD='password',
     MASTER_LOG_FILE='mysql-bin.000084', 
     MASTER_LOG_POS=775;
```
### Запускаем репликацию
```
START SLAVE;
```
### Проверяем статус репликации
```
SHOW SLAVE STATUS\G;
```
#### Эти параметры должны быть "yes"
```
Slave_IO_Running: Yes
Slave_SQL_Running: Yes
```
#### Если нет ищи ошибки в Last_IO_Error:

## Переключения с SLAVE на MASTER

### На SLAVE оснавливаем репликацию
```
STOP SLAVE;
RESET SLAVE ALL;
```
### Мастер настраиваем как SLAVE ранее
## Готово теперь они поменялись ролями
