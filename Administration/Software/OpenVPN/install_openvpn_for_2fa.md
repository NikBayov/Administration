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
###
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
#### В итоге ваша директория /etc/openvpn должна содеражать:
![screenshot](/cache/picture/etc_ovpn.png)



