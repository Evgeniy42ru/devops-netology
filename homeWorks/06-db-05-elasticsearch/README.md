# Домашнее задание к занятию "6.5. Elasticsearch"

## Задача 1

>В этом задании вы потренируетесь в:
>- установке elasticsearch
>- первоначальном конфигурировании elastcisearch
>- запуске elasticsearch в docker
>
>Используя докер образ [centos:7](https://hub.docker.com/_/centos) как базовый и 
>[документацию по установке и запуску Elastcisearch](https://www.elastic.co/guide/en/elasticsearch/reference/current/targz.html):
>
>- составьте Dockerfile-манифест для elasticsearch
>- соберите docker-образ и сделайте `push` в ваш docker.io репозиторий
>- запустите контейнер из получившегося образа и выполните запрос пути `/` c хост-машины
>
>Требования к `elasticsearch.yml`:
>- данные `path` должны сохраняться в `/var/lib`
>- имя ноды должно быть `netology_test`
>
>В ответе приведите:
>- текст Dockerfile манифеста
>- ссылку на образ в репозитории dockerhub
>- ответ `elasticsearch` на запрос пути `/` в json виде
>
>Подсказки:
>- возможно вам понадобится установка пакета perl-Digest-SHA для корректной работы >пакета shasum
>- при сетевых проблемах внимательно изучите кластерные и сетевые настройки в >elasticsearch.yml
>- при некоторых проблемах вам поможет docker директива ulimit
>- elasticsearch в логах обычно описывает проблему и пути ее решения
>
>Далее мы будем работать с данным экземпляром elasticsearch.

### Ответ:
- Текст Dockerfile манифеста ./elasticsearch/Dockerfile
- [Образ в репозитории dockerhub](https://hub.docker.com/repository/docker/evgeniy42ru/netology-devops-elasticsearch)
```
docker login -u evgeniy42ru
docker build -t centos7test .
docker tag 418118f9549b evgeniy42ru/netology-devops-elasticsearch
docker push  evgeniy42ru/netology-devops-elasticsearch
```
- Ответ `elasticsearch` на запрос пути `/` в json виде
``` shell
#запускаем контейнер
docker run -p 127.0.0.1:9200:9200/tcp -it centos7test

#запускаем elasticsearch
su -u elasticsearch /elasticsearch-8.5.3/bin/elasticsearch

#выполняем запрос к elasticsearch
curl \
  --request GET -sL \
  --url 'http://localhost:9200/' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json"
---
{
  "name" : "netology_test",
  "cluster_name" : "elasticsearch-cluster",
  "cluster_uuid" : "9IUol4tOQC2TC06U14DmBw",
  "version" : {
    "number" : "8.5.3",
    "build_flavor" : "default",
    "build_type" : "tar",
    "build_hash" : "4ed5ee9afac63de92ec98f404ccbed7d3ba9584e",
    "build_date" : "2022-12-05T18:22:22.226119656Z",
    "build_snapshot" : false,
    "lucene_version" : "9.4.2",
    "minimum_wire_compatibility_version" : "7.17.0",
    "minimum_index_compatibility_version" : "7.0.0"
  },
  "tagline" : "You Know, for Search"
}
```


## Задача 2

>В этом задании вы научитесь:
>- создавать и удалять индексы
>- изучать состояние кластера
>- обосновывать причину деградации доступности данных
>
>Ознакомтесь с [документацией](https://www.elastic.co/guide/en/elasticsearch/reference/current/indices-create-index.html) 
и добавьте в `elasticsearch` 3 индекса, в соответствии со таблицей:
>
>| Имя | Количество реплик | Количество шард |
>|-----|-------------------|-----------------|
>| ind-1| 0 | 1 |
>| ind-2 | 1 | 2 |
>| ind-3 | 2 | 4 |
>
>Получите список индексов и их статусов, используя API и **приведите в ответе** на задание.
>
>Получите состояние кластера `elasticsearch`, используя API.
>
>Как вы думаете, почему часть индексов и кластер находится в состоянии yellow?
>
>Удалите все индексы.
>
>**Важно**
>
>При проектировании кластера elasticsearch нужно корректно рассчитывать количество реплик и шард,
иначе возможна потеря данных индексов, вплоть до полной, при деградации системы.

### Ответ:
- Создаём индексы
``` shell
# Создаём ind-1
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/ind-1' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
        "settings": {
          "index": {
            "number_of_shards": 1,  
            "number_of_replicas": 0 
        }
      }
    }'
---
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-1"}

# Создаём ind-2
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/ind-2' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
       "settings": {
        "index": {
          "number_of_shards": 2,  
          "number_of_replicas": 1 
        }
      }
    }'
---
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-2"}

# Создаём ind-3
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/ind-3' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
       "settings": {
        "index": {
          "number_of_shards": 4,  
          "number_of_replicas": 2 
        }
      }
    }'
---
{"acknowledged":true,"shards_acknowledged":true,"index":"ind-3"}
```
- Получаяем состояние кластера
``` shell
# Запрос
curl \
  --request GET \
  -sL \
  --url 'http://localhost:9200/_cluster/health' \
  -H "Contenstate: application/json"
---
{"cluster_name":"elasticsearch-cluster","status":"yellow","timed_out":false,"number_of_nodes":1,"number_of_data_nodes":1,"active_primary_shards":8,"active_shards":8,"relocating_shards":0,"initializing_shards":0,"unassigned_shards":10,"delayed_unassigned_shards":0,"number_of_pending_tasks":0,"number_of_in_flight_fetch":0,"task_max_waiting_in_queue_millis":0,"active_shards_percent_as_number":44.44444444444444}

# Запрос
curl \
  --request GET \
  -sL \
  --url 'http://localhost:9200/_cat/indices' \
  -H "Content-Type: application/json"
---
green  open ind-1 WNMsi-scSAKEKT17FKlWsQ 1 0 0 0 225b 225b
yellow open ind-3 lwK-2DeFT0OZKiyKkHlShg 4 2 0 0 900b 900b
yellow open ind-2 xv_Hl-7kRPqf2dfRCkMw8Q 2 1 0 0 450b 450b
```

- Часть индексов имеет статус yellow, в кластере только один сервер elasticsearch, у индексов в конфигурации несколько реплик а реплицироваться некуда.

- Удаляем индексы
``` shell
# Удаляем ind-1
curl \
  --request DELETE -sL \
  --url 'http://localhost:9200/ind-1' \
  -H "Content-Type: application/json"
---
{"acknowledged":true}

# Удаляем ind-2
curl \
  --request DELETE -sL \
  --url 'http://localhost:9200/ind-2' \
  -H "Content-Type: application/json"
---
{"acknowledged":true}

# Удаляем ind-3
curl \
  --request DELETE -sL \
  --url 'http://localhost:9200/ind-3' \
  -H "Content-Type: application/json"
---
{"acknowledged":true}
```

## Задача 3

>В данном задании вы научитесь:
>- создавать бэкапы данных
>- восстанавливать индексы из бэкапов
>
>Создайте директорию `{путь до корневой директории с elasticsearch в образе}/snapshots`.
>
>Используя API [зарегистрируйте](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-register-repository.html#snapshots-register-repository) 
>данную директорию как `snapshot repository` c именем `netology_backup`.
>
>**Приведите в ответе** запрос API и результат вызова API для создания репозитория.
>
>Создайте индекс `test` с 0 реплик и 1 шардом и **приведите в ответе** список индексов.
>
>[Создайте `snapshot`](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-take-snapshot.html) 
>состояния кластера `elasticsearch`.
>
>**Приведите в ответе** список файлов в директории со `snapshot`ами.
>
>Удалите индекс `test` и создайте индекс `test-2`. **Приведите в ответе** список индексов.
>
>[Восстановите](https://www.elastic.co/guide/en/elasticsearch/reference/current/snapshots-restore-snapshot.html) состояние
>кластера `elasticsearch` из `snapshot`, созданного ранее. 
>
>**Приведите в ответе** запрос к API восстановления и итоговый список индексов.
>
>Подсказки:
>- возможно вам понадобится доработать `elasticsearch.yml` в части директивы `path.repo` и перезапустить `elasticsearch`

Ответ:
- Регистрируем `snapshot repository` c именем `netology_backup`
``` shell
#Запрос
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/_snapshot/netology_backup' \
  -H "Content-Type: application/json" \
  -d '{
        "type": "fs",
        "settings": {
        "location": "/elasticsearch-8.5.3/snapshot/"
        }
      }'
---
{"acknowledged":true}
```

- Создаём индекс test
``` shell
#Запрос
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/test' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
        "settings": {
          "index": {
            "number_of_shards": 1,  
            "number_of_replicas": 0 
        }
      }
    }'
---
{"acknowledged":true,"shards_acknowledged":true,"index":"test"}
```

- Список индексов
``` shell
curl \
  --request GET \
  -sL \
  --url 'http://localhost:9200/_cat/indices' \
  -H "Content-Type: application/json"
---
green open test 4W1uwsfmTsmDrmeB5c4Pkg 1 0 0 0 225b 225b
```

- Создаём `snapshot`
```
curl \
     --request PUT \
     -sL \
     --url 'http://localhost:9200/_snapshot/netology_backup/%3Cmy_snapshot_%7Bnow%2Fd%7D%3E?wait_for_completion=true&pretty=true' \
     -H "Content-Type: application/json" \
     -d '{
          "indices": ["test"],
          "ignore_unavailable": true,
          "include_global_state": false
        }'
---
{
  "snapshot" : {
    "snapshot" : "my_snapshot_2023.01.07",
    "uuid" : "OFpEQRpVTamROndCZEsx3Q",
    "repository" : "netology_backup",
    "version_id" : 8050399,
    "version" : "8.5.3",
    "indices" : [
      "test"
    ],
    "data_streams" : [ ],
    "include_global_state" : false,
    "state" : "SUCCESS",
    "start_time" : "2023-01-07T17:48:52.408Z",
    "start_time_in_millis" : 1673113732408,
    "end_time" : "2023-01-07T17:48:52.408Z",
    "end_time_in_millis" : 1673113732408,
    "duration_in_millis" : 0,
    "failures" : [ ],
    "shards" : {
      "total" : 1,
      "failed" : 0,
      "successful" : 1
    },
    "feature_states" : [ ]
  }
}
```
- Список файло в директории `snapshot`
``` shell
[root@3860a58f8a56 snapshot]# pwd
/elasticsearch-8.5.3/snapshot
[root@3860a58f8a56 snapshot]# ls -la
total 32
drwxrwxr-- 1 elasticsearch root          4096 Jan  7 17:48 .
drwxr-xr-x 1 elasticsearch elasticsearch 4096 Jan  5 12:19 ..
-rw-rw-r-- 1 elasticsearch elasticsearch  598 Jan  7 17:48 index-0
-rw-rw-r-- 1 elasticsearch elasticsearch    8 Jan  7 17:48 index.latest
drwxrwxr-x 3 elasticsearch elasticsearch 4096 Jan  7 17:48 indices
-rw-rw-r-- 1 elasticsearch elasticsearch  212 Jan  7 17:48 meta-OFpEQRpVTamROndCZEsx3Q.dat
-rw-rw-r-- 1 elasticsearch elasticsearch  313 Jan  7 17:48 snap-OFpEQRpVTamROndCZEsx3Q.dat
```

- Удалите индекс test и создайте индекс test-2. Приведите в ответе список индексов.
``` shell
# Удаляем индекс test
curl \
  --request DELETE -sL \
  --url 'http://localhost:9200/test' \
  -H "Content-Type: application/json"
---
{"acknowledged":true}

# Создаём индекс test-2
curl \
  --request PUT \
  -sL \
  --url 'http://localhost:9200/test-2' \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
        "settings": {
          "index": {
            "number_of_shards": 1,  
            "number_of_replicas": 0 
        }
      }
    }'
---
{"acknowledged":true,"shards_acknowledged":true,"index":"test-2"}

# Cписок индексов
curl \
  --request GET \
  -sL \
  --url 'http://localhost:9200/_cat/indices' \
  -H "Content-Type: application/json"
---
green open test-2 -VdNtVXjRaqjhzKxSd6BJA 1 0 0 0 225b 225b
```

- Восстанавливаем состояние кластера elasticsearch из snapshot, созданного ранее.
``` shell
# Доступные `snapshot`
curl \
  --request GET -sL \
  --url 'http://localhost:9200/_snapshot/netology_backup/*?verbose=false&pretty=true' \
  -H "Content-Type: application/json"
---
{
  "snapshots" : [
    {
      "snapshot" : "my_snapshot_2023.01.07",
      "uuid" : "OFpEQRpVTamROndCZEsx3Q",
      "repository" : "netology_backup",
      "indices" : [
        "test"
      ],
      "data_streams" : [ ],
      "state" : "SUCCESS"
    }
  ],
  "total" : 1,
  "remaining" : 0
}

# Востанавливаем
curl \
  --request POST -sL \
  --url 'http://localhost:9200/_snapshot/netology_backup/my_snapshot_2023.01.07/_restore' \
  -H "Content-Type: application/json"
---
{"accepted":true}

# Проверяем индексы
curl \
  --request GET -sL \
  --url 'http://localhost:9200/_cat/indices' \
  -H "Content-Type: application/json" 
---
green open test-2 -VdNtVXjRaqjhzKxSd6BJA 1 0 0 0 225b 225b
green open test   sQb2xQ6xTY6Nmtxa03th-g 1 0 0 0 225b 225b
```