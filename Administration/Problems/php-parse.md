### Необходимо проверить версию php чтоб каманда была php7.1  а не php
`for server in $CLUSTER; do if [ ${#PROJECT_PATH} -ge 10 ]; then ssh ${server} "php71 ${PROJECT_PATH}simple.php System/Cache/clear"; break; fi; done`
