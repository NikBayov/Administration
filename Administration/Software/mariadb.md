sudo apt-get install software-properties-common -y
sudo apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc'
sudo add-apt-repository 'deb [arch=amd64] https://archive.mariadb.org/mariadb-10.4/repo/debian buster main'
sudo apt update
sudo apt install mariadb-server -y
