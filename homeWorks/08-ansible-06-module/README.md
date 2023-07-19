# [Домашнее задание к занятию 6 «Создание собственных модулей»](https://github.com/netology-code/mnt-homeworks/blob/MNT-video/08-ansible-06-module/README.md)

## Подготовка к выполнению

### 1.
>Создайте пустой публичный репозиторий в своём любом проекте: `my_own_collection`.

Создал - https://github.com/Evgeniy42ru/my_own_collection

### 2.
>Скачайте репозиторий Ansible: `git clone https://github.com/ansible/ansible.git` по любому, удобному вам пути.

[Скачал](./ansible/)

### 3.
>Зайдите в директорию Ansible: `cd ansible`.

-

### 4.
>Создайте виртуальное окружение: `python3 -m venv venv`.

```shell
python3 -m venv venv
```

### 5.
>Активируйте виртуальное окружение: `. venv/bin/activate`. Дальнейшие действия производятся только в виртуальном окружении.
```shell
ansible % . venv/bin/activate
(venv) ansible %
```

### 6.
>Установите зависимости `pip install -r requirements.txt`.
```shell
ansible % pip install -r requirements.txt
Ignoring importlib_resources: markers 'python_version < "3.10"' don't match your environment
Collecting jinja2>=3.0.0
  Using cached Jinja2-3.1.2-py3-none-any.whl (133 kB)
Collecting PyYAML>=5.1
  Downloading PyYAML-6.0-cp311-cp311-macosx_11_0_arm64.whl (167 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 167.5/167.5 kB 727.0 kB/s eta 0:00:00
Collecting cryptography
  Using cached cryptography-41.0.1-cp37-abi3-macosx_10_12_universal2.whl (5.3 MB)
Collecting packaging
  Using cached packaging-23.1-py3-none-any.whl (48 kB)
Collecting resolvelib<1.1.0,>=0.5.3
  Using cached resolvelib-1.0.1-py2.py3-none-any.whl (17 kB)
Collecting MarkupSafe>=2.0
  Using cached MarkupSafe-2.1.3-cp311-cp311-macosx_10_9_universal2.whl (17 kB)
Collecting cffi>=1.12
  Using cached cffi-1.15.1-cp311-cp311-macosx_11_0_arm64.whl (174 kB)
Collecting pycparser
  Using cached pycparser-2.21-py2.py3-none-any.whl (118 kB)
Installing collected packages: resolvelib, PyYAML, pycparser, packaging, MarkupSafe, jinja2, cffi, cryptography
Successfully installed MarkupSafe-2.1.3 PyYAML-6.0 cffi-1.15.1 cryptography-41.0.1 jinja2-3.1.2 packaging-23.1 pycparser-2.21 resolvelib-1.0.1

[notice] A new release of pip is available: 23.0.1 -> 23.1.2
[notice] To update, run: pip install --upgrade pip
```
### 7.
>Запустите настройку окружения `. hacking/env-setup`.
```shell
ansible % . hacking/env-setup
gen_egg_info:3: no matches found: /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/lib/ansible*.egg-info
running egg_info
creating lib/ansible_core.egg-info
writing lib/ansible_core.egg-info/PKG-INFO
writing dependency_links to lib/ansible_core.egg-info/dependency_links.txt
writing entry points to lib/ansible_core.egg-info/entry_points.txt
writing requirements to lib/ansible_core.egg-info/requires.txt
writing top-level names to lib/ansible_core.egg-info/top_level.txt
writing manifest file 'lib/ansible_core.egg-info/SOURCES.txt'
reading manifest file 'lib/ansible_core.egg-info/SOURCES.txt'
reading manifest template 'MANIFEST.in'
adding license file 'COPYING'
writing manifest file 'lib/ansible_core.egg-info/SOURCES.txt'

Setting up Ansible to run out of checkout...

PATH=/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/bin:/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/venv/bin:/opt/homebrew/bin:/opt/homebrew/sbin:/Users/Evgeniy/Library/Python/3.8/bin:/Users/Evgeniy/yandex-cloud/bin:/usr/local/bin:/System/Cryptexes/App/usr/bin:/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/go/bin:/Users/Evgeniy/Library/Python/3.8/bin:/Users/Evgeniy/yandex-cloud/bin:/Users/Evgeniy/Library/Application Support/JetBrains/Toolbox/scripts:/Users/Evgeniy/Library/Application Support/JetBrains/Toolbox/scripts
PYTHONPATH=/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/test/lib:/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/lib
MANPATH=/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/ansible/ansible/docs/man:/opt/homebrew/share/man::

Remember, you may wish to specify your host file with -i

Done!
```
### 8.
>Если все шаги прошли успешно — выйдите из виртуального окружения `deactivate`.
```shell
(venv) Evgeniy@192 ansible % deactivate
Evgeniy@192 ansible %
```
### 9.
>Ваше окружение настроено. Чтобы запустить его, нужно находиться в директории `ansible` и выполнить конструкцию `. venv/bin/activate && . hacking/env-setup`.

## Основная часть

Ваша цель — написать собственный module, который вы можете использовать в своей role через playbook. Всё это должно быть собрано в виде collection и отправлено в ваш репозиторий.

### **Шаг 1.**  
>В виртуальном окружении создайте новый `my_own_module.py` файл.

Создал - [my_own_module.py](./ansible/ansible/lib/ansible/modules/my_own_module.py)

### **Шаг 2.**
>Наполните его содержимым:

```python
#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_test

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: This is the message to send to the test module.
        required: true
        type: str
    new:
        description:
            - Control to demo if the result of this module is changed or not.
            - Parameter description can be a list as well.
        required: false
        type: bool
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - my_namespace.my_collection.my_doc_fragment_name

author:
    - Your Name (@yourGitHubHandle)
'''

EXAMPLES = r'''
# Pass in a message
- name: Test with a message
  my_namespace.my_collection.my_test:
    name: hello world

# pass in a message and have changed true
- name: Test with a message and changed output
  my_namespace.my_collection.my_test:
    name: hello world
    new: true

# fail the module
- name: Test failure of the module
  my_namespace.my_collection.my_test:
    name: fail me
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
original_message:
    description: The original name param that was passed in.
    type: str
    returned: always
    sample: 'hello world'
message:
    description: The output message that the test module generates.
    type: str
    returned: always
    sample: 'goodbye'
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        new=dict(type='bool', required=False, default=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    result['original_message'] = module.params['name']
    result['message'] = 'goodbye'

    # use whatever logic you need to determine whether or not this module
    # made any modifications to your target
    if module.params['new']:
        result['changed'] = True

    # during the execution of the module, if there is an exception or a
    # conditional state that effectively causes a failure, run
    # AnsibleModule.fail_json() to pass in the message and the result
    if module.params['name'] == 'fail me':
        module.fail_json(msg='You requested this to fail', **result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
```
>Или возьмите это наполнение [из статьи](https://docs.ansible.com/ansible/latest/dev_guide/developing_modules_general.html#creating-a-module).

Наполнил содержимым - [my_own_module.py](./ansible/ansible/lib/ansible/modules/my_own_module.py)


### **Шаг 3.**
>Заполните файл в соответствии с требованиями Ansible так, чтобы он выполнял основную задачу: module должен создавать текстовый файл на удалённом хосте по пути, определённом в параметре `path`, с содержимым, определённым в параметре `content`.

Заполнил и перенёс файл - [my_own_module.py](./ansible/ansible/lib/ansible/modules/my_own_module.py)

### **Шаг 4.** 
>Проверьте module на исполняемость локально.

Для теста модуля создал файл c входными данными для теста модуля [payload.json](./ansible/ansible/payload.json)

Локальный запуск модуля:
```shell
(venv) Evgeniy@192 ansible % python -m ansible.modules.my_own_module payload.json

{"changed": false, "original_message": "/tmp/test_text.txt, test content", "message": "/tmp/test_text.txt, test context", "invocation": {"module_args": {"path": "/tmp/test_text.txt", "content": "test content"}}}
```

### **Шаг 5.**  
>Напишите single task playbook и используйте module в нём.

Написал - [playbook.yml](./ansible/ansible/playbook.yml)

### **Шаг 6.** 
>Проверьте через playbook на идемпотентность.

Проверяю на идемпотентность:
```shell
(venv) Evgeniy@192 ansible % ansible-playbook playbook.yml --diff                    
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can
become unstable at any point.
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [My own module] *****************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [localhost]

TASK [Call my_own_module] ************************************************************************************************
ok: [localhost]

PLAY RECAP ***************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```

### **Шаг 7.** 
>Выйдите из виртуального окружения.

Выхожу:
```shell
(venv) Evgeniy@192 ansible % deactivate
Evgeniy@192 ansible % 
```

### **Шаг 8.**
>Инициализируйте новую collection: `ansible-galaxy collection init my_own_namespace.yandex_cloud_elk`.

Инициализировал:
```shell
Evgeniy@192 08-ansible-06-module % ansible-galaxy collection init netology.yandex_cloud_elk
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can
become unstable at any point.
- Collection netology.yandex_cloud_elk was created successfully
```

### **Шаг 9.**
>В эту collection перенесите свой module в соответствующую директорию.

Cоздаём директорию для переноса модуля в сollection:
```shell
Evgeniy@192 08-ansible-06-module % mkdir ./netology/yandex_cloud_elk/plugins/modules
```

Перенёс модуль [my_own_module.py](./netology/yandex_cloud_elk/plugins/modules/my_own_module.py)


### **Шаг 10.**
>Single task playbook преобразуйте в single task role и перенесите в collection. У role должны быть default всех параметров module.

Преобразовал в single task role и перенёс в collection [my_own_role](./netology/yandex_cloud_elk/roles/my_own_role/)

### **Шаг 11.**
>Создайте playbook для использования этой role.

Создал playbook для использования этой role - [playbook_for_role](./netology/yandex_cloud_elk/playbook_for_role.yml)
Проверил выполнение:
```shell
vgeniy@192 yandex_cloud_elk % ansible-playbook playbook_for_role.yml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can
become unstable at any point.
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match
'all'

PLAY [My own role] *******************************************************************************************************

TASK [Gathering Facts] ***************************************************************************************************
ok: [localhost]

TASK [my_own_role : Call my_own_module] **********************************************************************************
ok: [localhost]

PLAY RECAP ***************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0  
```

### **Шаг 12.**
>Заполните всю документацию по collection, выложите в свой репозиторий, поставьте тег `1.0.0` на этот коммит.

Выложил - [1.0.0](https://github.com/Evgeniy42ru/my_own_collection/releases/tag/1.0.0)

### **Шаг 13.**
>Создайте .tar.gz этой collection: `ansible-galaxy collection build` в корневой директории collection.

Создал архив:
```shell
Evgeniy@192 yandex_cloud_elk % ansible-galaxy collection build
Created collection for netology.yandex_cloud_elk at /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-06-module/netology/yandex_cloud_elk/netology-yandex_cloud_elk-1.0.0.tar.gz
```

### **Шаг 14.**
>Создайте ещё одну директорию любого наименования, перенесите туда single task playbook и архив c collection.

Создал директорию [collection_from_the_archive](./collection_from_the_archive/) и перенёс туда [архив](./collection_from_the_archive/netology-yandex_cloud_elk-1.0.0.tar.gz)  и [single task playbook](./collection_from_the_archive/playbook.yml)

### **Шаг 15.**
>Установите collection из локального архива: `ansible-galaxy collection install <archivename>.tar.gz`.

Установил collection из локального архива:
```shell
Evgeniy@192 collection_from_the_archive % ansible-galaxy collection install netology-yandex_cloud_elk-1.0.0.tar.gz
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'netology.yandex_cloud_elk:1.0.0' to '/Users/Evgeniy/.ansible/collections/ansible_collections/netology/yandex_cloud_elk'
netology.yandex_cloud_elk:1.0.0 was installed successfully
```

### **Шаг 16.**
>Запустите playbook, убедитесь, что он работает.

Запустил - работает.
```shell
Evgeniy@192 collection_from_the_archive % ansible-playbook playbook.yml
[WARNING]: You are running the development version of Ansible. You should only run Ansible from "devel" if you are
modifying the Ansible engine, or trying out features under development. This is a rapidly changing source of code and can
become unstable at any point.
[WARNING]: No inventory was parsed, only implicit localhost is available
[WARNING]: provided hosts list is empty, only localhost is available. Note that the implicit localhost does not match 'all'

PLAY [My own module] *******************************************************************************************************

TASK [Gathering Facts] *****************************************************************************************************
ok: [localhost]

TASK [Call my_own_module] **************************************************************************************************
ok: [localhost]

PLAY RECAP *****************************************************************************************************************
localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0 
```



### **Шаг 17.** 
>В ответ необходимо прислать ссылки на collection и tar.gz архив, а также скриншоты выполнения пунктов 4, 6, 15 и 16.

В README.md подробно описал каждый шаг выполнения HW и приложил результат выполнения команд, думаю это лучше скриншотов.

---