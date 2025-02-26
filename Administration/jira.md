```docker-compose.yml
version: '3.8'
 
services:
  # Jira service
  jira:
    image: atlassian/jira-software:9.6.0
    container_name: jira
    ports:
      - "8080:8080"
      - "8091:8081"
    environment:
      - ATL_JDBC_URL=jdbc:postgresql://jira-postgres:5432/jiradb
      - ATL_JDBC_USER=jirauser
      - ATL_JDBC_PASSWORD=124578Qz1
      - ATL_DB_TYPE=postgresql
      - SETENV_JVM_MINIMUM_MEMORY=2048m
      - SETENV_JVM_MAXIMUM_MEMORY=4096m
      - VIRTUAL_PORT=8080
    volumes:
      - ./volumes/jira_home_update:/var/atlassian/application-data/jira:rw
      - ./crack:/crack
    depends_on:
      - jira-postgres
    networks:
      - jira_network
 
  # Jira PostgreSQL service
  jira-postgres:
    image: postgres:13
    container_name: jira-postgres
    environment:
      - POSTGRES_DB=jiradb
      - POSTGRES_USER=jirauser
      - POSTGRES_PASSWORD=124578Qz1
    volumes:
      - jira_postgres_data:/var/lib/postgresql/data
    networks:
      - jira_network
 
  # Confluence service
  confluence:
    image: atlassian/confluence-server:7.12.3
    container_name: confluence
    ports:
      - "8090:8090"
    environment:
      - ATL_JDBC_URL=jdbc:postgresql://confluence-postgres:5432/confluencedb
      - ATL_JDBC_USER=confluenceuser
      - ATL_JDBC_PASSWORD=124578Qz1
      - ATL_DB_TYPE=postgresql
    volumes:
      - confluence_data:/var/atlassian/application-data/confluence
    depends_on:
      - confluence-postgres
    networks:
      - confluence_network
 
  # Confluence PostgreSQL service
  confluence-postgres:
    image: postgres:13
    container_name: confluence-postgres
    environment:
      - POSTGRES_DB=confluencedb
      - POSTGRES_USER=confluenceuser
      - POSTGRES_PASSWORD=124578Qz1
    volumes:
      - confluence_postgres_data:/var/lib/postgresql/data
    networks:
      - confluence_network
 
volumes:
  jira_data:
  jira_postgres_data:
  confluence_data:
  confluence_postgres_data:
 
networks:
  jira_network:
  confluence_network:

```

### После переходим по http://ip:8080 и следуем инструкциям
### Когда выходит окно активации
```bash
rm -f /opt/atlassian/jira/atlassian-jira/WEB-INF/lib/atlassian-extras-3.4.6.jar # заходим в контейнер jira
docker cp atlassian-extras-3.4.6.jar 1ef5e956bd99:///opt/atlassian/jira/atlassian-jira/WEB-INF/lib # копируем файл  в контейнер jira
```
### Вводим лицуху
```
AAAB+g0ODAoPeJyNU12PojAUfedXkOzjBmzRwY+kySriyIo6DrCT9a3iVTrD17bFGffXLwhmPjRmE15o7zn3nHNvv3lFqg5zrmKkImOA+wNkqoFvqQYyDGXPAdIoy3PgustCSAX4xxwWNAFiLedz+9Fyhq5icaCSZemYSiAVUEMdDSPlBmQMIuQsr1AkSGOWMAlbNa4B6uaoRlLmYtBq/Y1YDDrLlDllqYSUpiHYbznjx6Zbr6+hbvkpz4zTs0p7y2rqhevMHd8eK4si2QBf7gIBXBANn8Xd4Mp5ti1CqVc/msh28pVy0C+IbtTSULIDEMkL+JTlx/Mb8FIVtaB0zevSJp5fZePKnKF4xeY9xlOJfaBxcRoG2dFYNPRfiZZ8T1Mm6roq6TJo3G/ruIN1bJg6xr1BDyGsWFkqS7F2GX5MhJ7oz/RAt6y8+rFPyjM9zJK6xUUsjdgpFRGZW8iarKxJ27v/zhLjPnl9Sqcrx/Lcdb4wZv31ygmmeBYf//xOWiNv7XaXuwhPneDhpZV1Ealb/GdqnqS8clr7b8bsjInrjD17obnY7PTv7rq4Y5oIf9qaa4vqAT8AL+Gj0ZOtIfcn1oKlMdEc358pL3A8DwObCHVRr93G117N5T4+FDyMqICvb+Yj+DSxnDPRmC7lkysWmiGdlI+G/j+VCElqMCwCFGxrnjz1G0V5MDwiLbn3gPiP6BUqAhRxlZk+6MN8sZsehGcEYqlhbQxMyg==X02o0
```
### Всё готово
