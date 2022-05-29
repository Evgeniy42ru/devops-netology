# Домашнее задание к занятию ["4.2. Использование Python для решения типовых DevOps задач"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-02-py)

## Обязательная задача 1

Есть скрипт:
```python
#!/usr/bin/env python3
a = 1
b = '2'
c = a + b
```

### Вопросы:
| Вопрос  | Ответ |
| ------------- | ------------- |
| Какое значение будет присвоено переменной `c`?  | ``` unsupported operand type(s) for +: 'int' and 'str' c = a + b ```
|
| Как получить для переменной `c` значение 12?  | `c = str(a) + b`  |
| Как получить для переменной `c` значение 3?  | `c = a + int(b)`  |

## Обязательная задача 2
Мы устроились на работу в компанию, где раньше уже был DevOps Engineer. Он написал скрипт, позволяющий узнать, какие файлы модифицированы в репозитории, относительно локальных изменений. Этим скриптом недовольно начальство, потому что в его выводе есть не все изменённые файлы, а также непонятен полный путь к директории, где они находятся. Как можно доработать скрипт ниже, чтобы он исполнял требования вашего руководителя?

```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/netology/sysadm-homeworks", "git status"]
result_os = os.popen(' && '.join(bash_command)).read()
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(prepare_result)
        break
```

### Ваш скрипт:
```python
#!/usr/bin/env python3

import os

bash_command = ["cd ~/Projects/netology/devops-netology", "git status"]
bash_command_pwd = ["cd ~/Projects/netology/devops-netology", "pwd"]
result_os = os.popen(' && '.join(bash_command)).read()
general_path = os.popen(' && '.join(bash_command_pwd)).read().rstrip('\n')
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(general_path + '/' + prepare_result)
```

### Вывод скрипта при запуске при тестировании:
```
Evgeniy@192 4.2_py % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/2_script.py
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/2_script.py
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/readme.md
```

## Обязательная задача 3
1. Доработать скрипт выше так, чтобы он мог проверять не только локальный репозиторий в текущей директории, а также умел воспринимать путь к репозиторию, который мы передаём как входной параметр. Мы точно знаем, что начальство коварное и будет проверять работу этого скрипта в директориях, которые не являются локальными репозиториями.

### Ваш скрипт:
```python
#!/usr/bin/env python3


import os
import sys


#Проверяем что указан путь к репозиторию
try:
    repoPath = sys.argv[1]
except IndexError:
    print("Необходимо указать путь к репозиторию.")
    exit(1)

#Проверяем что директория существует
if os.path.exists(repoPath) == False:
    print ("Директории не существует - " + repoPath)
    exit(1)

#Проверяем наличие гита 
bash_command = ["cd " + repoPath, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()

if (result_os) == 'fatal: not a git repository (or any of the parent directories): .git':
    print(result_os)
    exit(1)

#Проверяем изменения
bash_command_pwd = ["cd " + repoPath, "pwd"]
general_path = os.popen(' && '.join(bash_command_pwd)).read().rstrip('\n')
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(general_path + '/' + prepare_result)
        #break
```

### Вывод скрипта при запуске при тестировании:
```
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/2_script.py
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/readme.md
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/         
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/2_script.py
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/readme.md
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /Users/Evgeniy/Projects/netology/devops-netology/          
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/2_script.py
/Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/readme.md
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /Users/Evgeniy/Projects/netology/                
fatal: not a git repository (or any of the parent directories): .git
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /                                
fatal: not a git repository (or any of the parent directories): .git
Evgeniy@192 devops-netology % 
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py  
Необходимо указать путь к репозиторию.
Evgeniy@192 devops-netology % 
Evgeniy@192 devops-netology % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/3_scrypt.py /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/not_exist_directory 
Директории не существует - /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/not_exist_directory
```

## Обязательная задача 4
1. Наша команда разрабатывает несколько веб-сервисов, доступных по http. Мы точно знаем, что на их стенде нет никакой балансировки, кластеризации, за DNS прячется конкретный IP сервера, где установлен сервис. Проблема в том, что отдел, занимающийся нашей инфраструктурой очень часто меняет нам сервера, поэтому IP меняются примерно раз в неделю, при этом сервисы сохраняют за собой DNS имена. Это бы совсем никого не беспокоило, если бы несколько раз сервера не уезжали в такой сегмент сети нашей компании, который недоступен для разработчиков. Мы хотим написать скрипт, который опрашивает веб-сервисы, получает их IP, выводит информацию в стандартный вывод в виде: <URL сервиса> - <его IP>. Также, должна быть реализована возможность проверки текущего IP сервиса c его IP из предыдущей проверки. Если проверка будет провалена - оповестить об этом в стандартный вывод сообщением: [ERROR] <URL сервиса> IP mismatch: <старый IP> <Новый IP>. Будем считать, что наша разработка реализовала сервисы: `drive.google.com`, `mail.google.com`, `google.com`.

### Ваш скрипт:
```python
#!/usr/bin/env python3


import json
import socket
import time


needChangeIps = False

with open('hosts.json') as json_file:
    hosts = json.load(json_file)

for host in hosts:
    ipActual = socket.gethostbyname(host)
    
    if hosts[host] != ipActual:
        print("[ERROR] {} IP mismatch: {} {}".format(host, hosts[host], ipActual))
        hosts[host] = ipActual
        needChangeIps = True
    else:
        print("{} - {}".format(host, hosts[host]))

if needChangeIps == True:
    with open('hosts.json', 'w') as outfile:
        json.dump(hosts, outfile)
```

### Вывод скрипта при запуске при тестировании:
```
#Изначально указал в файле hosts.json все адреса 0.0.0.0 чтобы сразу поймать ошибку.
Evgeniy@192 4.2_py % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/4_scrypt.py
[ERROR] drive.google.com IP mismatch: 0.0.0.0 64.233.164.194
[ERROR] mail.google.com IP mismatch: 0.0.0.0 64.233.165.18
[ERROR] google.com IP mismatch: 0.0.0.0 142.251.1.102
Evgeniy@192 4.2_py % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/4_scrypt.py
drive.google.com - 64.233.164.194
mail.google.com - 64.233.165.18
google.com - 142.251.1.102
Evgeniy@192 4.2_py % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.2_py/4_scrypt.py
drive.google.com - 64.233.164.194
mail.google.com - 64.233.165.18
google.com - 142.251.1.102
Evgeniy@192 4.2_py % 
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так получилось, что мы очень часто вносим правки в конфигурацию своей системы прямо на сервере. Но так как вся наша команда разработки держит файлы конфигурации в github и пользуется gitflow, то нам приходится каждый раз переносить архив с нашими изменениями с сервера на наш локальный компьютер, формировать новую ветку, коммитить в неё изменения, создавать pull request (PR) и только после выполнения Merge мы наконец можем официально подтвердить, что новая конфигурация применена. Мы хотим максимально автоматизировать всю цепочку действий. Для этого нам нужно написать скрипт, который будет в директории с локальным репозиторием обращаться по API к github, создавать PR для вливания текущей выбранной ветки в master с сообщением, которое мы вписываем в первый параметр при обращении к py-файлу (сообщение не может быть пустым). При желании, можно добавить к указанному функционалу создание новой ветки, commit и push в неё изменений конфигурации. С директорией локального репозитория можно делать всё, что угодно. Также, принимаем во внимание, что Merge Conflict у нас отсутствуют и их точно не будет при push, как в свою ветку, так и при слиянии в master. Важно получить конечный результат с созданным PR, в котором применяются наши изменения. 

### Ваш скрипт:
```python
???
```

### Вывод скрипта при запуске при тестировании:
```
???
```