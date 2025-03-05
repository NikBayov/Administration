# Настройка двух интерфейсов внешний и локальный

### Настраивает внешний интерфейс ens192

```
nano /etc/sysconfig/network-scripts/ifcfg-ens192
```
```
DEVICE=ens192
TYPE=Ethernet
ONBOOT=yes
NM_CONTROLLED=no
BOOTPROTO=static
IPADDR=<внешний ip>
NETMASK=255.255.255.128
```
### Настраиваем локальный интрерфейс ens224
```
nano /etc/sysconfig/network-scripts/ifcfg-ens224
```
```
TYPE=Ethernet
BOOTPROTO=none
DEFROUTE=yes
PEERDNS=yes
PEERROUTES=yes
IPV4_FAILURE_FATAL=no
IPV6INIT=no
IPV6_AUTOCONF=yes
IPV6_DEFROUTE=yes
IPV6_PEERDNS=yes
IPV6_PEERROUTES=yes
IPV6_FAILURE_FATAL=no
IPV6_ADDR_GEN_MODE=stable-privacy
NAME=ens224
UUID=8c26d11c-6d7e-433e-8d6b-793aca7e80b9
DEVICE=ens224
ONBOOT=yes
IPADDR0=<local-ip>
PREFIX0=<netmask> пример 25
GATEWAY0=<>
DNS1=<>
DNS2=<>
```
### Добавляем таблици
```
nano /etc/iproute2/rt_tables
```
```
# reserved values
#
172     lan
185     wan
255     local
254     main
253     default
0       unspec
#100 ens192_table
#200 ens224_table

#
# local
#
#1      inr.ruhep
```
### Настраиваем правила для ens192
```nano /etc/sysconfig/network-scripts/route-ens192
<broadcast> via <external-ip> dev ens192
default table 185 via <external-gateway>
```
```nano /etc/sysconfig/network-scripts/rule-ens192
from <external-ip> table 185
```
### Тоже настриваем для ens224
```nano /etc/sysconfig/network-scripts/route-ens224
default table 172 via <local-gateway>
```
```nano /etc/sysconfig/network-scripts/rule-ens224
from <local-ip> table 172
```

### Запускаем nat
```
sudo iptables -t nat -A POSTROUTING -o ens192 -j MASQUERADE
iptables-save > /etc/sysconfig/iptables
```

### Перезагружаем машину для проверки
```
reboot 0
```
