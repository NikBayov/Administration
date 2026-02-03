# Сломалось ВМ Debian12, после скрин:
![screenshot](/cache/picture/filesystem_crush.png)
### В командной строке (initramfs) выполните:
```bash
fsck /dev/mapper/debian12-vg-root
```
### 2. При появлении вопросов:

Обычно отвечайте y (yes) на все вопросы о восстановлении
Если спросит про backup inode tables - можно ответить n (no)

### 3. После восстановления:

Когда fsck завершится:
```bash
exit
```
