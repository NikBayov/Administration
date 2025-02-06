# Добавление LDAP-авторизации

### Устанавливаем ldap-utils
```
sudo apt-get install ldap-utils
```
### Изменяем принцип авторизации в скрипте /etc/openvpn/oath.sh
```bash
#!/bin/bash

# Скрипт для проверки MFA с использованием oathtool и LDAP

passfile=$1

# Проверка, что файл с паролем передан и существует
if [ -z "$passfile" ] || [ ! -f "$passfile" ]; then
    echo "Passfile not provided or does not exist"
    exit 1
fi

# Получение имени пользователя и пароля из временного файла
user=$(head -1 "$passfile")
pass=$(tail -1 "$passfile")

# Добавление домена, если он отсутствует
if [[ "$user" != *@* ]]; then
    user="${user}@<your_domain>"
fi

# Проверка, что имя пользователя и пароль получены
if [ -z "$user" ] || [ -z "$pass" ]; then
    echo "USER_OR_PASS_NOT_FOUND"
    exit 1
fi

# Поиск записи в файле oath.secrets, игнорируя регистр
secret=$(grep -i -m 1 "^${user}:" /etc/openvpn/oath.secrets | cut -d: -f2)

# Проверка, что секрет найден
if [ -z "$secret" ]; then
    echo "USER_NOT_FOUND"
    exit 1
fi

# Вычисление ожидаемого кода
code=$(oathtool --totp "$secret")

# Проверка, содержит ли пароль разделитель для пароля и MFA
if echo "$pass" | grep -q ":"; then
    realpass=$(echo "$pass" | cut -d: -f1)
    mfatoken=$(echo "$pass" | cut -d: -f2)

    # Проверка пароля пользователя через LDAP
    ldapsearch -x -H ldap://<your_domain>:3268 -D "$user" "(givenName=$user)" -w "$realpass" > /dev/null 2>&1
    ldap_status=$?

    if [ $ldap_status -eq 0 ] && [ "$mfatoken" = "$code" ]; then
        echo "$user" >> "$session_file"
        echo "Authentication successful"
        exit 0
    fi
else
    # Если пароль не содержит разделителя, проверяем только MFA токен
    if [ "$pass" = "$code" ]; then
        echo "$user" >> "$session_file"
        echo "Authentication successful"
        exit 0
    fi
fi

# Если мы дошли до этого места, аутентификация не удалась
echo "Authentication failed"
exit 1
```

### Должен быть доступ вашей к локальной сети у /etc/openvpn/server.conf
```
push "route 172.17.0.0 255.255.0.0"
push "dhcp-option DNS <ip-local-dns-server>"
push "dhcp-option DNS 8.8.8.8"
```

