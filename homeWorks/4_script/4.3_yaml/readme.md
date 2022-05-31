# Домашнее задание к занятию ["4.3. Языки разметки JSON и YAML"](https://github.com/netology-code/sysadm-homeworks/tree/devsys10/04-script-03-yaml)


## Обязательная задача 1
Мы выгрузили JSON, который получили через API запрос к нашему сервису:
```
    { "info" : "Sample JSON output from our service\t",
        "elements" :[
            { "name" : "first",
            "type" : "server",
            "ip" : 7175 
            }
            { "name" : "second",
            "type" : "proxy",
            "ip : 71.78.22.43
            }
        ]
    }
```
Нужно найти и исправить все ошибки, которые допускает наш сервис  

Исправленный Json
```
{ 
    "info" : "Sample JSON output from our service\t",
    "elements" :[
        {
            "name" : "first",
            "type" : "server",
            "ip" : 7175 
        },
        { 
            "name" : "second",
            "type" : "proxy",
            "ip" : "71.78.22.43"
        }
    ]
}
```
## Обязательная задача 2
В прошлый рабочий день мы создавали скрипт, позволяющий опрашивать веб-сервисы и получать их IP. К уже реализованному функционалу нам нужно добавить возможность записи JSON и YAML файлов, описывающих наши сервисы. Формат записи JSON по одному сервису: `{ "имя сервиса" : "его IP"}`. Формат записи YAML по одному сервису: `- имя сервиса: его IP`. Если в момент исполнения скрипта меняется IP у сервиса - он должен так же поменяться в yml и json файле.

### Ваш скрипт:
```python
#!/usr/bin/env python3


import json
import socket
import yaml


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

    with open('hosts.yaml', 'w') as outfile:
        yaml.dump(hosts, outfile)
```

### Вывод скрипта при запуске при тестировании:
```
Evgeniy@192 4.3_yaml % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.3_yaml/1_scrypt.py
[ERROR] drive.google.com IP mismatch: 0.0.0.0 64.233.164.194
[ERROR] mail.google.com IP mismatch: 0.0.0.0 216.58.207.197
[ERROR] google.com IP mismatch: 0.0.0.0 142.250.74.78
Evgeniy@192 4.3_yaml % /usr/bin/python3 /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/4_script/4.3_yaml/1_scrypt.py
drive.google.com - 64.233.164.194
mail.google.com - 216.58.207.197
google.com - 142.250.74.78
```

### json-файл(ы), который(е) записал ваш скрипт:
```json
{"drive.google.com": "64.233.164.194", "mail.google.com": "216.58.207.197", "google.com": "142.250.74.78"}
```

### yml-файл(ы), который(е) записал ваш скрипт:
```yaml
drive.google.com: 64.233.164.194
google.com: 142.250.74.78
mail.google.com: 216.58.207.197
```

## Дополнительное задание (со звездочкой*) - необязательно к выполнению

Так как команды в нашей компании никак не могут прийти к единому мнению о том, какой формат разметки данных использовать: JSON или YAML, нам нужно реализовать парсер из одного формата в другой. Он должен уметь:
   * Принимать на вход имя файла
   * Проверять формат исходного файла. Если файл не json или yml - скрипт должен остановить свою работу
   * Распознавать какой формат данных в файле. Считается, что файлы *.json и *.yml могут быть перепутаны
   * Перекодировать данные из исходного формата во второй доступный (из JSON в YAML, из YAML в JSON)
   * При обнаружении ошибки в исходном файле - указать в стандартном выводе строку с ошибкой синтаксиса и её номер
   * Полученный файл должен иметь имя исходного файла, разница в наименовании обеспечивается разницей расширения файлов

### Ваш скрипт:
```python
???
```

### Пример работы скрипта:
???