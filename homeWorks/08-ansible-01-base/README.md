# Домашнее задание к занятию 1 «Введение в Ansible»

## Подготовка к выполнению

>1. Установите Ansible версии 2.10 или выше.    

pip установлен ранее
```shell
python3 -m pip -V
pip 21.2.4 from /Library/Developer/CommandLineTools/Library/Frameworks/Python3.framework/Versions/3.9/lib/python3.9/site-packages/pip (python 3.9)
```
Устанавливаем ansible
```shell
python3 -m pip install --user ansible

ansible --version
ansible [core 2.14.4]
  config file = None
  configured module search path = ['/Users/Evgeniy/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /Users/Evgeniy/Library/Python/3.9/lib/python/site-packages/ansible
  ansible collection location = /Users/Evgeniy/.ansible/collections:/usr/share/ansible/collections
  executable location = /Users/Evgeniy/Library/Python/3.8/bin/ansible
  python version = 3.9.6 (default, Oct 18 2022, 12:41:40) [Clang 14.0.0 (clang-1400.0.29.202)] (/Library/Developer/CommandLineTools/usr/bin/python3)
  jinja version = 3.1.2
  libyaml = True
```
>2. Создайте свой публичный репозиторий на GitHub с произвольным именем.
- https://github.com/Evgeniy42ru/devops-netology
>3. Скачайте [Playbook](./playbook/) из репозитория с домашним заданием и перенесите его в свой репозиторий.
- https://github.com/Evgeniy42ru/devops-netology/tree/main/homeWorks/08-ansible-01-base/playbook

## Основная часть

>1. Попробуйте запустить playbook на окружении из `test.yml`, зафиксируйте значение, которое имеет факт `some_fact` для указанного хоста при выполнении playbook.

Ответ: 12
```shell
ansible-playbook site.yml -i inventory/test.yml

PLAY [Print os facts] ********************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************
[WARNING]: Platform darwin on host localhost is using the discovered Python interpreter at /usr/bin/python3, but future installation of another Python
interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-core/2.14/reference_appendices/interpreter_discovery.html for more
information.
ok: [localhost]

TASK [Print OS] **************************************************************************************************************************************************
ok: [localhost] => {
    "msg": "MacOSX"
}

TASK [Print fact] ************************************************************************************************************************************************
ok: [localhost] => {
    "msg": 12
}

PLAY RECAP *******************************************************************************************************************************************************
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

>2. Найдите файл с переменными (group_vars), в котором задаётся найденное в первом пункте значение, и поменяйте его на `all default fact`.

Ответ:
- Файл https://github.com/Evgeniy42ru/devops-netology/tree/main/homeWorks/08-ansible-01-base/playbook/group_vars/all/examp.yml
```shell
cat group_vars/all/examp.yml 
---
  some_fact: 12%       

#изменил значение
cat group_vars/all/examp.yml                   
---
  some_fact: "all default fact"% 
```

>3. Воспользуйтесь подготовленным (используется `docker`) или создайте собственное окружение для проведения дальнейших испытаний.

Ответ:
```shell
# запускаю контейнеры
docker run -dit --name centos7 pycontribs/centos:7 sleep 6000000
docker run -dit --name ubuntu pycontribs/ubuntu:latest sleep 6000000

# проверяю
docker ps
CONTAINER ID   IMAGE                      COMMAND           CREATED         STATUS         PORTS     NAMES
5c50c95f1ba0   pycontribs/ubuntu:latest   "sleep 6000000"   2 minutes ago   Up 2 minutes             ubuntu
185d3ba129cb   pycontribs/centos:7        "sleep 6000000"   3 minutes ago   Up 3 minutes             centos7
---
```

>4. Проведите запуск playbook на окружении из `prod.yml`. Зафиксируйте полученные значения `some_fact` для каждого из `managed host`.

Ответ:
- [centos7] => {"msg": "el"}
- [ubuntu] => {"msg": "deb"}
```shell
ansible-playbook site.yml -i inventory/prod.yml

PLAY [Print os facts] ********************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el"
}
ok: [ubuntu] => {
    "msg": "deb"
}

PLAY RECAP *******************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

5. Добавьте факты в `group_vars` каждой из групп хостов так, чтобы для `some_fact` получились значения: для `deb` — `deb default fact`, для `el` — `el default fact`.

Ответ:
```shell
cat group_vars/deb/examp.yml && cat group_vars/el/examp.yml 
---
  some_fact: "deb default fact"
---
  some_fact: "el default fact"%  
```
6.  Повторите запуск playbook на окружении `prod.yml`. Убедитесь, что выдаются корректные значения для всех хостов.

Ответ: значения выдаются корректные.
```shell
ansible-playbook site.yml -i inventory/prod.yml            

PLAY [Print os facts] ********************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *******************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

7. При помощи `ansible-vault` зашифруйте факты в `group_vars/deb` и `group_vars/el` с паролем `netology`.

Ответ:
```shell
ansible-vault encrypt group_vars/deb/examp.yml
New Vault password: 
Confirm New Vault password: 
Encryption successful
---

ansible-vault encrypt group_vars/el/examp.yml
New Vault password: 
Confirm New Vault password: 
Encryption successful
```

8. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь в работоспособности.

Ответ:
```shell
ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] ********************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}

TASK [Print fact] ************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}

PLAY RECAP *******************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```
>9. Посмотрите при помощи `ansible-doc` список плагинов для подключения. Выберите подходящий для работы на `control node`.

Ответ: https://docs.ansible.com/ansible/latest/plugins/connection.html
- You can use ansible-doc -t connection -l to see the list of available plugins. Use ansible-doc -t connection <plugin name> to see detailed documentation and examples.
```shell
ansible-doc -t connection local        
> ANSIBLE.BUILTIN.LOCAL    (/Users/Evgeniy/Library/Python/3.9/lib/python/site-packages/ansible/plugins/connection/local.py)

        This connection plugin allows ansible to execute tasks on the Ansible 'controller' instead of on a remote host.

ADDED IN: historical

OPTIONS (= is mandatory):

- pipelining
        Pipelining reduces the number of connection operations required to execute a module on the remote server, by executing
        many Ansible modules without actual file transfers.
        This can result in a very significant performance improvement when enabled.
        However this can conflict with privilege escalation (become). For example, when using sudo operations you must first
        disable 'requiretty' in the sudoers file for the target hosts, which is why this feature is disabled by default.
        set_via:
          env:
          - name: ANSIBLE_PIPELINING
          ini:
          - key: pipelining
            section: defaults
          - key: pipelining
            section: connection
          vars:
          - name: ansible_pipelining
        default: false
        type: boolean


NOTES:
      * The remote user is ignored, the user with which the ansible CLI was executed is used instead.


AUTHOR: ansible (@core)

NAME: local
```
>10. В `prod.yml` добавьте новую группу хостов с именем  `local`, в ней разместите localhost с необходимым типом подключения.

Ответ:
```
playbook % cat inventory/prod.yml 
---
  el:
    hosts:
      centos7:
        ansible_connection: docker
  deb:
    hosts:
      ubuntu:
        ansible_connection: docker
  mac:
    hosts:
      localhost:
        ansible_connection: local
```

11. Запустите playbook на окружении `prod.yml`. При запуске `ansible` должен запросить у вас пароль. Убедитесь, что факты `some_fact` для каждого из хостов определены из верных `group_vars`.

Ответ:
```shell
ansible-playbook site.yml -i inventory/prod.yml --ask-vault-pass
Vault password: 

PLAY [Print os facts] ********************************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************************************
[WARNING]: Platform darwin on host localhost is using the discovered Python interpreter at /usr/bin/python3, but future installation of another Python
interpreter could change the meaning of that path. See https://docs.ansible.com/ansible-core/2.14/reference_appendices/interpreter_discovery.html for more
information.
ok: [localhost]
ok: [ubuntu]
ok: [centos7]

TASK [Print OS] **************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "CentOS"
}
ok: [ubuntu] => {
    "msg": "Ubuntu"
}
ok: [localhost] => {
    "msg": "MacOSX"
}

TASK [Print fact] ************************************************************************************************************************************************
ok: [centos7] => {
    "msg": "el default fact"
}
ok: [ubuntu] => {
    "msg": "deb default fact"
}
ok: [localhost] => {
    "msg": "all default fact"
}

PLAY RECAP *******************************************************************************************************************************************************
centos7                    : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   
ubuntu                     : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

>12. Заполните `README.md` ответами на вопросы. Сделайте `git push` в ветку `master`. В ответе отправьте ссылку на ваш открытый репозиторий с изменённым `playbook` и заполненным `README.md`.

Ответ: https://github.com/Evgeniy42ru/devops-netology/tree/main/homeWorks/08-ansible-01-base/README.md

---