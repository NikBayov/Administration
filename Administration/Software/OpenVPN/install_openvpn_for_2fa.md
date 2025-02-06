# Установка OpenVPN-server для двухфакторной аутентификации(Debian 12)

### Устанавливаем необходимые пакеты

```
sudo apt update
sudo apt install openvpn oathtool qrencode curl nano -y
```

### Устанавливаем структуру ключей easyrsa3

```
mkdir /src; cd /src && wget https://github.com/OpenVPN/easy-rsa/archive/master.zip
apt install unzip
unzip master.zip
cd easy-rsa-master/easyrsa3
./easyrsa init-pki
```

#### Создаём центр сертификации
`./easyrsa build-ca`
##### В процессе вы получите запрос на ввод пароля от 4 до 32 символов, сохраните его, он нам потребуется в будущем:
![screenshot](/cache/picture/ca_ovpn.png)
##### В процессе вы получите запрос на ввод общего имени, вводите название для группы, её будут использовать все клиенты
![screenshot](/cache/picture/ca_ovpn1.png)
#### Теперь генерируем запрос на создание сертификата, чтобы в дальнейшем подключаться к серверу без пароля
`./easyrsa gen-req <server-name> nopass`
#### Подписываем запрос, будет запрошен пароль. Используем пароль, который сохранили при создании центра сертификации
`./easyrsa sign-req server <server-name>`
#### Генерируем общий сертификат для клиентов(CN тот что задали):
```
./easyrsa gen-req <client-shared> nopass
./easyrsa sign-req client <client-shared>
```
#### Генерируем файл с параметрами Диффи-Хеллмана (dh.pem):
`./easyrsa gen-dh`
#### Генерируем tls-сертификат
```
openvpn --genkey secret /etc/openvpn/tls-crypt.key
```
### Переносим полученные сертификаты
```
mv ./pki/dh.pem /etc/openvpn/dh1024.pem
mv ./pki/private/<client-shared>.key /etc/openvpn/
mv ./pki/private/<server-name>.key /etc/openvpn/
mv ./pki/ca.crt /etc/openvpn/
mv ./pki/issued/<client-shared>.crt /etc/openvpn/
mv ./pki/issued/<server-name>.crt /etc/openvpn/
```

### Скачиваем архив 
```
wget https://github.com/NikBayov/Administration/tree/main/cache/Archives/openvpn.zip
unzip openvpn.zip
cp -R openvpn /etc/openvpn
```
#### В итоге ваша директория /etc/openvpn должна содержать:
![screenshot](/cache/picture/etc_ovpn.png)

##### В server.conf можете указать подсеть в которой будет выдавать ip-адреса openvpn, у меня 192.168.8.0 
`server 192.168.8.0 255.255.255.0`

### Создание пользователей

#### в файл user_credentials.txt прописываем нужного пользователя в формате `username:password`
```
echo n.bayov@example.com:12345678 >> /etc/openvpn/user_credentials.txt
```
#### с помощью скрипта oath-secret-gen.sh генерируем секрет для созданного пользователя
```
./oath-secret-gen.sh n.bayov@examle.com
```
#### добавляем последнюю строку в файл /etc/openvpn/oath.secrets
```
echo n.bayov@example.com:3173a5c8242af43738bbb9ca90d9d7 >> /etc/openvpn/oath.secrets
```
#### Генерируем qrcode для любого otp приложения(google authenticator и т.д., яндекс ключ не советую)
```
qrencode -o otp_qr.png otpauth://totp/MFA%20Sample:n.bayov@example.com?secret=GFZ2LSBEFL2DOOF3XHFJBWOX
```
##### Проверка генерации TOTP вручную
```
oathtool --totp <secret>
oathtool --totp 3173a5c8242af43738bbb9ca90d9d7 # пример
```
##### Если есть iptables
```
iptables -t nat -A POSTROUTING -s 192.168.8.0/24 -o eth0 -j MASQUERADE
echo 1 > /proc/sys/net/ipv4/ip_forward
```
#### Запускаем openvpn-server и проверяем, что нет ошибок

```
systemctl start openvpn@server
systemctl status openvpn@server
```
### Д 

### Создаём конфиг клиента 
```
remote <your_external_ip_server> 1194
dev tun
proto udp4
client
verb 4
keepalive 10 60
persist-tun
auth-user-pass
remote-cert-tls server
<ca>
-----BEGIN CERTIFICATE-----
ваш /etc/openvpn/ca.crt
-----END CERTIFICATE-----
</ca>
<cert>
-----BEGIN CERTIFICATE-----
ваш /etc/openvpn/client-shared.crt
-----END CERTIFICATE-----
</cert>
<key>
-----BEGIN PRIVATE KEY-----
ваш /etc/openvpn/client-shared.key
-----END PRIVATE KEY-----
</key>
```
### Настройка iptables
```
apt-get install iptables-persistent iptables # установка iptables
iptables -I INPUT -p udp --dport 1194 -m state --state NEW -j ACCEPT # открытие порта 1194 udp для vpn-сервера
```
#### Использование NAT,если необходим
```
sudo iptables -t nat -A POSTROUTING -s 10.10.11.0/24 -d 172.17.0.0/16 -j SNAT --to-source 192.168.0.2
# 192.168.0.2 -> ip vpn-server
# 192.168.0.2 -> подсеть к которой нужен доступ
# 10.10.11.0/24 -> виртуальная подсеть vpn сервера 
```
### Режим отладки авторизации
```
tail -f /var/log/mfa_openvpn.log
```
### Проверка аторизации
#### Добавить в скрипт /etc/openvpn/oath.sh
```
     echo "User: $user"
     echo "Real Password: $realpass"
     echo "MFA Token: $mfatoken"
     echo "Generated TOTP Code: $code"
```
#### Вводим логин n<пароль>:код и проверяем результат
```
echo -e "n.bayov@example.com\n12345678:898137" > /tmp/test_passfile
./oath.sh /tmp/test_passfile
```
