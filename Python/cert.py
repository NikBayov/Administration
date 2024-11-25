# Запрашиваем $domen.ru$ и $test.domen.ru$
# Выпускаем сертификат на основной домен
iptables -I INPUT -p tcp -m tcp --dport 80 -j ACCEPT # Открываем порт
# Добавляем блок кода в конфиг по пути /etc/nginx/conf.d/letsencrypt.conf 
server {
  listen 80;
  server_name $domen.ru$; #меняем на нужное нам доменное имя
  root /var/www/app2;
  location / {
  index index.html;
  try_files $uri $uri/index.html;
  }
}
# Далее проверяем конфиг nginx если ошибок нет, то продолжаем, если нет скрипт прерывается
nginx -t 
# Если предыдущий шаг прошел, тогда перечитываем конфигурацию
nginx -s reload 
# Проверяем выпуск сертификата, если ошибок нет продолжаем
certbot certonly --webroot -w /var/www/app2 -d $domen.ru$ --dry-run
# Для сертификатов без приписки test и dev стандартно используется путь /var/www/app2
# После выполнения прошлого шага, и получения вывода об успешном тестовом выпуске сертификата, выполняем следующую команду, которая начнёт процесс выпуска сертификата:
certbot certonly --webroot -w /var/www/app2 -d $domen.ru$
# После запуска команды, нам будет предложено, с какого сервера выпустить сертификат.
# Выбираем любой, разницы нет.
# После того, как мы выпустили сертификат, проверяем его наличие на сервере 172.17.25.131(доступы: login:root passwd:K.nsqGBYUDBY)512) по пути /etc/nginx/certs/$domen.ru$ 
# После выпускаем тестовый сертификат на тестовый домен
# Выполняем команду на выпуск сертификата:
# Часть /var/www/test/$domen$/web , тут указывается фактическая директория 
certbot certonly --webroot -w /var/www/test/$domen$/web -d $test.domen.ru$
# Переходим к редактирования конфигурационных файлов на s-for1 ssh:172.17.0.18 root K.nsqGBYUDBY)512)   
#Редактирование конфигурационного файла $domen$
#Переходим в расположение /etc/puppetlabs/code/environments/cluster_frontend/modules/nginx/files/sites-enabled/prod_domen.conf , и находим необходимый нам конфигурационный файл.
#Далее, редактируем его, а именно, добавляем к уже имеющемуся блоку 80го порта, новый блок для 443
# Копируем уже готовый блок, и меняем порт с 80 на 443,  и дописываем пути до сертификатов
# Пути для сертификатов, необходимо искать на 172.17.25.131(доступы: login:root passwd:K.nsqGBYUDBY)512), это недействительно для доменов с test 
# Итоговый конфиг должен выглядеть примерно так
server {
  listen 80;
  server_name vk-sup-marusya.nextcontact.ru;
  root /var/www/vk-sup-marusya/web;
  include /etc/access/nextcontact_networks.acl;
  deny all;

  client_max_body_size 128m;

  index index.php;

  try_files $uri /index.php$is_args$args;

  location ~ ^/assets/.*\.php$ {
    deny all;
  }

  location ~ \.php$ {
    include fastcgi_params;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass backend-php7;
  }
}


server {
  listen 443 ssl;
  server_name vk-sup-marusya.nextcontact.ru;
  root /var/www/vk-sup-marusya/web;
  include /etc/access/nextcontact_networks.acl;
  deny all;
  ssl_certificate /etc/nginx/certs/vk-sup-marusya.nextcontact.ru/fullchain.pem;
  ssl_certificate_key /etc/nginx/certs/vk-sup-marusya.nextcontact.ru/privkey.pem;

  client_max_body_size 128m;

  index index.php;

  try_files $uri /index.php$is_args$args;

  location ~ ^/assets/.*\.php$ {
    deny all;
  }

  location ~ \.php$ {
    include fastcgi_params;
    fastcgi_index index.php;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass backend-php7;
  }
}
# Для домена с test, конфиг редактирутеся по пути /etc/nginx/conf.d/test_$domen$.conf
# Итоговый конфиг для домена с test или dev 
server {
  listen       443 ssl;
  server_name  out.lm-construction-leads.test.nextcontact.ru;
  root /var/www/test/lm-construction-leads/out/web;
ssl_certificate /etc/letsencrypt/live/out.lm-construction-leads.test.nextcontact.ru/fullchain.pem;
 ssl_certificate_key /etc/letsencrypt/live/out.lm-construction-leads.test.nextcontact.ru/privkey.pem;
#  include /etc/access/nextcontact_networks.acl;
#  deny all;
 
  client_max_body_size 128m;
 
  index index.php;
 
  try_files $uri /index.php$is_args$args;
 
  location ~ ^/assets/.*\.php$ {
        deny all;
  }
 
 location ~ \.php$ {
    include        fastcgi_params;
    fastcgi_index  index.php;
    fastcgi_param  SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_pass   127.0.0.1:9000;
  }
}
#Далее необходимо Переходим по доменным именам  out.lm-construction-leads.nextcontact.ru и out.lm-construction-leads.test.nextcontact.ru
#Проверяем наличие сертификатов
