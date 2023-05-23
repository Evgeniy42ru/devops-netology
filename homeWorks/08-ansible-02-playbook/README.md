# [Домашнее задание к занятию 2 «Работа с Playbook»](https://github.com/netology-code/mnt-homeworks/blob/MNT-video/08-ansible-02-playbook/README.md#домашнее-задание-к-занятию-2-работа-с-playbook)

## Подготовка к выполнению

>1. * Необязательно. Изучите, что такое [ClickHouse](https://www.youtube.com/watch?v=fjTNS2zkeBs) и [Vector](https://www.youtube.com/watch?v=CgEhyffisLY).

Ознакомился.

>2. Создайте свой публичный репозиторий на GitHub с произвольным именем или используйте старый.

https://github.com/Evgeniy42ru/devops-netology

>3. Скачайте [Playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.

https://github.com/Evgeniy42ru/devops-netology/tree/main/homeWorks/08-ansible-02-playbook

>4. Подготовьте хосты в соответствии с группами из предподготовленного playbook.

Ответ:
```shell
# запускаю контейнер
docker run -dit --name clickhouse-01 pycontribs/centos:7 sleep 6000000
---

# проверяю
docker ps
CONTAINER ID   IMAGE                 COMMAND           CREATED          STATUS          PORTS     NAMES
deede8e61fa7   pycontribs/centos:7   "sleep 6000000"   25 seconds ago   Up 24 seconds             clickhouse-01
---
```

## Основная часть

>### 1. Подготовьте свой inventory-файл `prod.yml`.
```yml
---
clickhouse:
  hosts:
    clickhouse-01:
      ansible_connection: docker
```
>### 2. Допишите playbook: нужно сделать ещё один play, который устанавливает и настраивает [vector](https://vector.dev).
```yml
- name: Install vector
  hosts: clickhouse-01
  tasks:
    - name: Get vector distrib
      ansible.builtin.get_url:
            url: "https://packages.timber.io/vector/0.30.0/vector-0.30.0-1.{{ vector_arch }}.rpm"
            dest: "./vector-0.30.0-1.{{ vector_arch }}.rpm"
    - name: Install vector
      ansible.builtin.yum:
        name:
          - vector-0.30.0-1.{{ vector_arch }}.rpm
      notify: Installed vector
```
>### 3. При создании tasks рекомендую использовать модули: `get_url`, `template`, `unarchive`, `file`.
>### 4. Tasks должны: скачать дистрибутив нужной версии, выполнить распаковку в выбранную директорию, установить vector.

>### 5. Запустите `ansible-lint site.yml` и исправьте ошибки, если они есть.

Сначала нужно установить `ansible-lint`
```shell
# устанавливаю ansible-lint
brew install ansible-lint
---

# проверяю
ansible-lint --version
ansible-lint 6.16.2 using ansible-core:2.14.6 ruamel-yaml:0.17.26 ruamel-yaml-clib:0.2.7
---
```

Запускаю проверку
```shell
ansible-lint site.yml
WARNING  Listing 7 violation(s) that are fatal
name[missing]: All tasks should be named.
site.yml:11 Task/Handler: block/always/rescue 

risky-file-permissions: File permissions unset or incorrect.
site.yml:12 Task/Handler: Get clickhouse distrib

risky-file-permissions: File permissions unset or incorrect.
site.yml:18 Task/Handler: Get clickhouse distrib

fqcn[action-core]: Use FQCN for builtin module actions (meta).
site.yml:30 Use `ansible.builtin.meta` or `ansible.legacy.meta` instead.

jinja[spacing]: Jinja2 spacing could be improved: create_db.rc != 0 and create_db.rc !=82 -> create_db.rc != 0 and create_db.rc != 82 (warning)
site.yml:32 Jinja2 template rewrite recommendation: `create_db.rc != 0 and create_db.rc != 82`.

risky-file-permissions: File permissions unset or incorrect.
site.yml:40 Task/Handler: Get vector distrib

yaml[indentation]: Wrong indentation: expected 8 but found 12
site.yml:42

Read documentation for instructions on how to ignore specific rule violations.

                    Rule Violation Summary                    
 count tag                    profile    rule associated tags 
     1 jinja[spacing]         basic      formatting (warning) 
     1 name[missing]          basic      idiom                
     1 yaml[indentation]      basic      formatting, yaml     
     3 risky-file-permissions safety     unpredictability     
     1 fqcn[action-core]      production formatting           

Failed after min profile: 6 failure(s), 1 warning(s) on 1 files.
```

Фикшу первую ошибку - отсутсвие имени у таски
```shell
name[missing]: All tasks should be named.
site.yml:11 Task/Handler: block/always/rescue
```
```yml
# Было
tasks:
    - block:
        - name: Get clickhouse distrib

# Стало
tasks:
    - name: Get clickhouse distributives
      block:
        - name: Get clickhouse distrib
```

Фикшу вторую ошибку - отсутсвие параметра `mode`, ansible не знает с какими правами создавать файл.
```shell
risky-file-permissions: File permissions unset or incorrect.
site.yml:12 Task/Handler: Get clickhouse distrib
```
```yml
# Было
- name: Get clickhouse distributives
      block:
        - name: Get clickhouse distrib
          ansible.builtin.get_url:
            url: "https://packages.clickhouse.com/rpm/stable/{{ item }}-{{ clickhouse_version }}.noarch.rpm"
            dest: "./{{ item }}-{{ clickhouse_version }}.rpm"
          with_items: "{{ clickhouse_packages }}"
      rescue:
        - name: Get clickhouse distrib
          ansible.builtin.get_url:
            url: "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-{{ clickhouse_version }}.x86_64.rpm"
            dest: "./clickhouse-common-static-{{ clickhouse_version }}.rpm"

# Стало
- name: Get clickhouse distributives
      block:
        - name: Get clickhouse distrib
          ansible.builtin.get_url:
            url: "https://packages.clickhouse.com/rpm/stable/{{ item }}-{{ clickhouse_version }}.noarch.rpm"
            dest: "./{{ item }}-{{ clickhouse_version }}.rpm"
            mode: "0755"
          with_items: "{{ clickhouse_packages }}"
      rescue:
        - name: Get clickhouse distrib
          ansible.builtin.get_url:
            url: "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-{{ clickhouse_version }}.x86_64.rpm"
            dest: "./clickhouse-common-static-{{ clickhouse_version }}.rpm"
            mode: "0755"
```

Фикшу третью ошибку
```
fqcn[action-core]: Use FQCN for builtin module actions (meta).
site.yml:33 Use `ansible.builtin.meta` or `ansible.legacy.meta` instead.
```

```yml
# Было
- name: Flush handlers
  meta: flush_handlers

# Стало
- name: Flush handlers
  ansible.builtin.meta: flush_handlers
```

Четвёртая ошибка - анологично второй ошибке, отсутсвие параметра `mode`
```shell
risky-file-permissions: File permissions unset or incorrect.
site.yml:43 Task/Handler: Get vector distrib
```

Пятая ошибка - неверное кол-во отступов.
```shell
yaml[indentation]: Wrong indentation: expected 8 but found 12
site.yml:45
```

Повторно запускаем `ansible-lint` после правок.
```shell
ansible-lint site.yml

Passed with production profile: 0 failure(s), 0 warning(s) on 1 files.
```



>### 6. Попробуйте запустить playbook на этом окружении с флагом `--check`.

Т.к. это симуляция - логично что падают таски которые используют файлы которые должны появится из предыдущих тасок.

https://docs.ansible.com/ansible/latest/playbook_guide/playbooks_checkmode.html - Check mode is just a simulation. It will not generate output for tasks that use conditionals based on registered variables (results of prior tasks).

```shell
ansible-playbook -i inventory/prod.yml site.yml --check

PLAY [Install Clickhouse] ********************************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01] => (item=clickhouse-client)
changed: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 1, "item": "clickhouse-common-static", "msg": "Request failed", "response": "HTTP Error 404: Not Found", "status_code": 404, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Install clickhouse packages] ***********************************************************************************************************************************************************************************************************************************************************************************************
fatal: [clickhouse-01]: FAILED! => {"changed": false, "msg": "No RPM file matching 'clickhouse-common-static-22.3.3.44.rpm' found on system", "rc": 127, "results": ["No RPM file matching 'clickhouse-common-static-22.3.3.44.rpm' found on system"]}

PLAY RECAP ***********************************************************************************************************************************************************************************************************************************************************************************************************************
clickhouse-01              : ok=2    changed=1    unreachable=0    failed=1    skipped=0    rescued=1    ignored=0 
```
>### 7. Запустите playbook на `prod.yml` окружении с флагом `--diff`. Убедитесь, что изменения на системе произведены.

Vector скачивается более 30 минут, хотя у него размер 39.2 MB. Из-за этого показалось что всё зависло, остановил выполнение playbook. Позже разобрался что всё ок и при повторном запуске установился vector, вывод в следующем пункте.
```shell
ansible-playbook -i inventory/prod.yml site.yml --diff 

PLAY [Install Clickhouse] ********************************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01] => (item=clickhouse-client)
changed: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 0, "item": "clickhouse-common-static", "msg": "Request failed", "response": "HTTP Error 404: Not Found", "status_code": 404, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] ****************************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Install clickhouse packages] ***********************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Flush handlers] ************************************************************************************************************************************************************************************************************************************************************************************************************

RUNNING HANDLER [Start clickhouse service] ***************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01]

TASK [Create database] ***********************************************************************************************************************************************************************************************************************************************************************************************************
changed: [clickhouse-01]

PLAY [Install vector] ************************************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ***********************************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get vector distrib] ********************************************************************************************************************************************************************************************************************************************************************************************************
^C [ERROR]: User interrupted execution
```

>### 8. Повторно запустите playbook с флагом `--diff` и убедитесь, что playbook идемпотентен.

Идемпотентен
```shell
ansible-playbook -i inventory/prod.yml site.yml --diff

PLAY [Install Clickhouse] ***************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get clickhouse distrib] ***********************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01] => (item=clickhouse-client)
ok: [clickhouse-01] => (item=clickhouse-server)
failed: [clickhouse-01] (item=clickhouse-common-static) => {"ansible_loop_var": "item", "changed": false, "dest": "./clickhouse-common-static-22.3.3.44.rpm", "elapsed": 1, "gid": 0, "group": "root", "item": "clickhouse-common-static", "mode": "0755", "msg": "Request failed", "owner": "root", "response": "HTTP Error 404: Not Found", "size": 246310036, "state": "file", "status_code": 404, "uid": 0, "url": "https://packages.clickhouse.com/rpm/stable/clickhouse-common-static-22.3.3.44.noarch.rpm"}

TASK [Get clickhouse distrib] ***********************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Install clickhouse packages] ******************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Flush handlers] *******************************************************************************************************************************************************************************************************************************************************************************************

TASK [Create database] ******************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

PLAY [Install vector] *******************************************************************************************************************************************************************************************************************************************************************************************

TASK [Gathering Facts] ******************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Get vector distrib] ***************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

TASK [Install vector] *******************************************************************************************************************************************************************************************************************************************************************************************
ok: [clickhouse-01]

PLAY RECAP ******************************************************************************************************************************************************************************************************************************************************************************************************
clickhouse-01              : ok=7    changed=0    unreachable=0    failed=0    skipped=0    rescued=1    ignored=0
```
>### 9. Подготовьте README.md-файл по своему playbook. В нём должно быть описано: что делает playbook, какие у него есть параметры и теги.

```yml
- name: Install vector # Имя самого play
  hosts: clickhouse # Группа хостов на которых будет выполнятся 
  tasks: # Таски которые будут выполнятся
    - name: Get vector distrib # Имя таски
      ansible.builtin.get_url: # Модуль ansible лдя скачивания файлов по url
        url: "https://packages.timber.io/vector/0.30.0/vector-0.30.0-1.{{ vector_arch }}.rpm" # url файла который нужно загрузить
        dest: "./vector-0.30.0-1.{{ vector_arch }}.rpm" # Указываем путь для сохранения загруженного файла
        mode: "0755" # Задаём права с которыми будет создан загруженный файл
    - name: Install vector # Имя таски
      ansible.builtin.yum: # Модуль ansible для установки через пакетный менеджер yum
        name: # Перечисляем имена пакетов для установки
          - vector-0.30.0-1.{{ vector_arch }}.rpm # Указываем rpm пакет для установки

```

>### 10. Готовый playbook выложите в свой репозиторий, поставьте тег `08-ansible-02-playbook` на фиксирующий коммит, в ответ предоставьте ссылку на него.

https://github.com/Evgeniy42ru/devops-netology/tree/main/homeWorks/08-ansible-02-playbook

---