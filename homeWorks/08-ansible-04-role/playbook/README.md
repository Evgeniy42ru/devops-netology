# Описание [playbook](./site.yml)

## Plays
- Install Clickhouse - установка и запуск Clickhouse
- Install Vector - установка и запуск Vector
- Install Lighthouse - установка и запуск Lighthouse, Nginx

## Tags
- `vector` по умолчанию выполняется, установлен на Play - `Install vector`
- `clickhouse` по умолчанию выполняется, установлен на Play - `Install Clickhouse`
- `lighthouse` по умолчанию выполняется, установлен на Play - `Install Lighthouse`

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

### Lighthouse
[lighthouse_vars.yml](./group_vars/lighthouse/lighthouse_vars.yml) тут мы указываем имя для nginx. Для lighthouse: репозиторий, версию(коммит), путь установки, имя логфайла.
```yml
---
nginx_username: evgeniy
lighthouse_vcs: https://github.com/VKCOM/lighthouse.git
lighthouse_vcs_version: d701335c25cd1bb9b5155711190bad8ab852c2ce
lighthouse_path: /var/www/lighthouse
lighthouse_access_log_name: lighthouse
```

## Группы хостов
[prod.yml](./inventory/prod.yml) 
```yml
---
clickhouse:
  hosts:
    clickhouse-01:
      ansible_host: {host_ip}
      ansible_user: {host_user}
vector:
  hosts:
    vector-01:
      ansible_host: {host_ip}
      ansible_user: {host_user}
lighthouse:
  hosts:
    lighthouse-01:
      ansible_host: {host_ip}
      ansible_user: {host_user}
```
У нас 3 группы хостов 
- `clickhouse` на все хосты данной группы будет установлен clickhouse.
- `vector` на все хосты данной группы будет установлен vector.
- `lighthouse` на все хосты данной группы будет установлен lighthouse и nginx.
