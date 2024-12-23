### Добавляем в файл конфигурации на сервере /etc/ssh/sshd_config: 

```
Ciphers aes256-gcm@openssh.com,chacha20-poly1305@openssh.com,aes128-ctr,aes192-ctr,aes256-ctr
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org,diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1
HostKeyAlgorithms ecdsa-sha2-nistp256,ssh-ed25519,ssh-rsa
PubkeyAcceptedKeyTypes +ssh-rsa
```

### На клиенте генерируем ключ с помощью команды:

`ssh-keygen -m PEM -t rsa`

### Скрипт php для проверки подключения:

 ```php
<?php
     $connection = ssh2_connect('ip.addres.ssh.server', 22, array(
         'hostkey' => 'ssh-rsa,ssh-dss',
         'kex' => 'diffie-hellman-group-exchange-sha256,diffie-hellman-group14-sha1',
         'client_to_server' => 'aes128-ctr,aes192-ctr,aes256-ctr',
         'server_to_client' => 'aes128-ctr,aes192-ctr,aes256-ctr'
     ));

if (!$connection)

{     die('Connection failed'); }
if (ssh2_auth_pubkey_file($connection, 'root',
                         '/root/.ssh/id_rsa.pub', #path to key
                         '/root/.ssh/id_rsa', 'passphrase')) #path to key

{     echo "Authentication Successful!\n"; }
else

{     echo "Authentication Failed...\n"; }
?>
```
