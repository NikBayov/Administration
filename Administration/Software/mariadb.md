sudo apt-get install software-properties-common -y
sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'
sudo add-apt-repository 'deb [arch=amd64] https://archive.mariadb.org/mariadb-10.4/repo/debian buster main'
sudo apt update
sudo apt install mariadb-server -y

sudo mkdir -p /var/log/mysql
sudo chown mysql:mysql /var/log/mysql
sudo chmod 755 /var/log/mysql

sudo touch /var/log/mysql/mariadb.log
sudo chown mysql:mysql /var/log/mysql/mariadb.log
sudo chmod 644 /var/log/mysql/mariadb.log
