# Расширение диска LVM(debian12)

### Заходим в диски и создаём новый part->write->yes->quit
```
cfdisk /dev/nvme0n1
```
### создаём физический том (PV) LVM на разделе nvme0n1p4
```
pvcreate /dev/nvme0n1p4
```
###  расширяем  группу томов (VG) debian12-vg, добавляя в неё PV nvme0n1p4
```
vgextend debian12-vg /dev/nvme0n1p4
```
### увеличиваем логический том (LV) root, используя всё свободное место в VG
```
lvextend -l +100%FREE /dev/debian12-vg/root
```
###  расширяем файловую систему ext4 внутри LV root до нового размера.
```
resize2fs /dev/debian12-vg/root
```
