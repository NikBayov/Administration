# Ошибки которые встретил в awx

### Ошибка с лимитами на воркерах
```
Failed to JSON parse a line from worker stream. Error: Expecting value: line 1 column 1 (char 0) Line with invalid JSON data: b'failed to create fsnotify watcher: too many open files\n'
```
## Решение
```
sudo sysctl -w fs.inotify.max_user_watches=2099999999
sudo sysctl -w fs.inotify.max_user_instances=2099999999
sudo sysctl -w fs.inotify.max_queued_events=2099999999
```
