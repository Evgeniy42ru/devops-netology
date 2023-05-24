# Описание [playbook](./site.yml)

## Содержание [playbook](./site.yml)

### Plays
-  Install Clickhouse
-  Install vector

### Tasks

#### Play - Install Clickhouse
Выполняется на группе хостов clickhouse указанных в - [prod.yml](./inventory/prod.yml)
- Get clickhouse distributives - скачивает дистрибутивы clickhouse версия и имена указанны в [clickhouse_vars.yml](./group_vars/clickhouse/clickhouse_vars.yml)
- Install clickhouse packages - устанавливает дистрибутивы clickhouse версия и имена указанны в [clickhouse_vars.yml](./group_vars/clickhouse/clickhouse_vars.yml)
- Flush handlers - вызывает hundlers, он у нас один Start clickhouse service - запускает сервис.
- Create database - выпоняет команду на создание DB в clickhouse

#### Play - Install vector
Выполняется на группе хостов vector указанных в - [prod.yml](./inventory/prod.yml)
- Get vector distrib - скачиваем дистрибутив vector версия указанна в [vector_vars.yml](./group_vars/vector/vector_vars.yml)
- Install vector - устанавливаем vector версия пакета указанна в [vector_vars.yml](./group_vars/vector/vector_vars.yml)
- Configure vector - конфигурируем vector, переменные конфига подставляемые в [шаблон](./template/vector/vector.toml.j2) конфигурационного файла указанны в [vector_vars.yml](./group_vars/vector/vector_vars.yml)

## Tags
- `vector` по умолчанию выполняется, установлен на Play - `Install vector`
- `clickhouse` по умолчанию выполняется, установлен на Play - `Install Clickhouse`

## Используемые переменные

Файлы со значениями переменных лежат в директории `playbook/group_vars`

### Clickhouse 
[clickhouse_vars.yml](./group_vars/clickhouse/clickhouse_vars.yml) тут мы указываем версию clickhouse которая будет установленна и пакеты.
```yml
---
clickhouse_version: "22.3.3.44"
clickhouse_packages:
  - clickhouse-client
  - clickhouse-server
  - clickhouse-common-static
```

### Vector 
[vector_vars.yml](./group_vars/vector/vector_vars.yml) тут мы указываем архитектуру rpm-пакета vector который будет скачен и далее установлен и тип sourse.in для конфигурации vector.
```yml
---
vector_arch: "x86_64"
sourse_in_type: "stdin"
```

## Группы хостов
[prod.yml](./inventory/prod.yml) 
```yml
---
clickhouse:
  hosts:
    clickhouse-01:
      ansible_connection: docker
vector:
  hosts:
    clickhouse-01:
      ansible_connection: docker
```
У нас две группы хостов 
- `clickhouse` на все хосты данной группы будет установлен clickhouse и его пакеты и далее запущен
- `vector` на все хосты данной группы будет установлен vector и сконфигурирован

Хост всего один `clickhouse-01` и он в обоих группах, ну так получилось, для теста в рамках домашней работы его хватает.


