# Устанавливаем php7.3 или любую другую старую версию на Debian12

### Устанавливаем нужные пакеты
```
sudo apt update && sudo apt install -y apt-transport-https ca-certificates lsb-release wget  alien libaio1 unzip -y
```
### Добавляем репозитории
```
wget -O- https://packages.sury.org/php/apt.gpg | sudo tee /etc/apt/trusted.gpg.d/sury-php.gpg
echo "deb https://packages.sury.org/php/ $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/php.list
```
### Устанавливаем php
```
sudo apt install -y php7.3 php7.3-cli php7.3-fpm php7.3-common php-pear php7.3-dev build-essential unzip
sudo apt install -y php7.3-{mbstring,xml,curl,mysql,zip,gd,intl,opcache,bz2,gmp,imap,ldap,soap,sqlite3,xml,pspell,redis,xdebug,mailparse,igbinary,pdo-sqlite}
```

### Установка Oracle-client
#### Скачиваем нужные нам пакеты с github
`https://github.com/dockette/oracle-instantclient/tree/master`
#### Я использую 19.6
```
oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
oracle-instantclient19.6-devel-19.6.0.0.0-1.x86_64.rpm
oracle-instantclient19.6-sqlplus-19.6.0.0.0-1.x86_64.rpm
oracle-instantclient19.6-tools-19.6.0.0.0-1.x86_64.rpm
instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip
```
#### Установка
```
sudo alien -i oracle-instantclient19.6-basic-19.6.0.0.0-1.x86_64.rpm
sudo alien -i oracle-instantclient19.6-devel-19.6.0.0.0-1.x86_64.rpm
sudo alien -i oracle-instantclient19.6-sqlplus-19.6.0.0.0-1.x86_64.rpm
sudo alien -i oracle-instantclient19.6-tools-19.6.0.0.0-1.x86_64.rpm
unzip instantclient-sdk-linux.x64-19.6.0.0.0dbru.zip /usr/lib/oracle/19.6/client64/
```
### Добавляем переменные 
```
echo "export ORACLE_HOME=/usr/lib/oracle/19.6/client64" >> ~/.bashrc
echo "export LD_LIBRARY_PATH=\$ORACLE_HOME/lib" >> ~/.bashrc
echo "export PATH=\$ORACLE_HOME/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc
```
#### Проверяем
```
ldd $ORACLE_HOME/lib/libclntsh.so
```
### Установка oci8 для php7.3(совместимые версии ищи в доке)
```bash
wget https://pecl.php.net/get/oci8-2.2.0.tgz
tar -xvzf oci8-2.2.0.tgz
cd oci8-2.2.0
phpize
./configure --with-oci8=instantclient,/usr/lib/oracle/19.6/client64/lib
make
sudo make install
echo "extension=oci8.so" | sudo tee /etc/php/7.3/mods-available/oci8.ini
phpenmod oci8
```
#### Проверяем 
```
php -m | grep oci8
```
### Устанавливаем pdo_oci
#### Клонируем репу php
```
git clone --branch PHP-7.3.3 https://github.com/php/php-src.git
```
#### Устанавливаем pdo_oci
```
cd ./php-src/ext/pdo_oci
phpize
./configure --with-pdo-oci=instantclient,/usr/lib/oracle/19.6/client64/lib
sudo make install
```
#### Создаём файл /etc/php/7.3/mods-available/pdo_oci.ini и добавляем в него:
```/etc/php/7.3/mods-available/pdo_oci.ini
extension=pdo_oci.so
```
#### Создаём симлинк
```
cd /etc/php/7.3/fpm/conf.d/
ln -s /etc/php/7.3/mods-available/pdo_oci.ini 20-pdo_oci.ini
```
