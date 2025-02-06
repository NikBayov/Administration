# Настройка логирования подключения и отключения клиентов vpn-сервера

### Создаём папку для скриптов логирования

```
mkdir /etc/openvpn/scripts
```
### Добавляем в неё скрипты
#### clent-connect.sh

```bash
#!/bin/bash

# Логирование подключения
echo "$(date '+%Y-%m-%d %H:%M:%S') - Client connected: $username, IP: $trusted_ip, VPN IP: $ifconfig_pool_remote_ip" >> /var/log/openvpn-connections.log

# Логирование для отладки
echo "Username: $username, Trusted IP: $trusted_ip" >> /var/log/openvpn-debug.log
```

#### client-disconnect.sh

```bash
#!/bin/bash

# Логирование отключения
echo "$(date '+%Y-%m-%d %H:%M:%S') - Client disconnected: $username, VPN IP: $ifconfig_pool_remote_ip" >> /var/log/openvpn-connections.log
echo "Common Name: $common_name" >> /var/log/openvpn-debug.log
echo "Username: $username" >> /var/log/openvpn-debug.log
```

### Добавлем строки в /etc/openvpn/server.conf

```
client-connect /etc/openvpn/scripts/client-connect.sh
client-disconnect /etc/openvpn/scripts/client-disconnect.sh
```

### Логи записываются в формате:
```bash
2025-02-05 15:35:58 - Client disconnected: n.bayov, VPN IP: 10.10.11.2
2025-02-06 09:32:11 - Client connected: n.bayov, IP: 109.195.28.55, VPN IP: 10.10.11.2`
```
