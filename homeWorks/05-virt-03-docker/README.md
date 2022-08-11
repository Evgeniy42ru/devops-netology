
# Домашнее задание к занятию ["5.3. Введение. Экосистема. Архитектура. Жизненный цикл Docker контейнера"](https://github.com/netology-code/virt-homeworks/tree/virt-11/05-virt-03-docker)

## Задача 1

Сценарий выполения задачи:

- создайте свой репозиторий на https://hub.docker.com;
- выберете любой образ, который содержит веб-сервер Nginx;
- создайте свой fork образа;
- реализуйте функциональность:
запуск веб-сервера в фоне с индекс-страницей, содержащей HTML-код ниже:
```
<html>
<head>
Hey, Netology
</head>
<body>
<h1>I’m DevOps Engineer!</h1>
</body>
</html>
```
Опубликуйте созданный форк в своем репозитории и предоставьте ответ в виде ссылки на https://hub.docker.com/username_repo.

>Ответ:  
Репозиторий: https://hub.docker.com/repository/docker/evgeniy42ru/netology-devops-nginx  
Команда запуска:  docker run --name ndn -p 80:80 -d evgeniy42ru/netology-devops-nginx:1.0.0

## Задача 2

Посмотрите на сценарий ниже и ответьте на вопрос:
"Подходит ли в этом сценарии использование Docker контейнеров или лучше подойдет виртуальная машина, физическая машина? Может быть возможны разные варианты?"

Детально опишите и обоснуйте свой выбор.

--

Сценарий:

- Высоконагруженное монолитное java веб-приложение;
>Ответ: docker подходит, удобно делать релизы путём подмены собранных контейнеров, возможность горизонтального маштабирование, простота в создании тестовой среды и локальной разработке.
- Nodejs веб-приложение;
>Ответ: аналогично с java приложением.
- Мобильное приложение c версиями для Android и iOS;
>Ответ: аналогично с java приложением.
- Шина данных на базе Apache Kafka;
>Ответ: ВМ, для оптимального утилизирования ресурсов, и удобного расширения кластера.
- Elasticsearch кластер для реализации логирования продуктивного веб-приложения - три ноды elasticsearch, два logstash и две ноды kibana;
>Ответ: ВМ по аналогии с Apache Kafka
- Мониторинг-стек на базе Prometheus и Grafana;
>Ответ: ВМ по аналогии с Apache Kafka
- MongoDB, как основное хранилище данных для java-приложения;
>Ответ: ФМ, т.к. это бд, не тратим ресурсы на виртуализацию.
- Gitlab сервер для реализации CI/CD процессов и приватный (закрытый) Docker Registry.
>Ответ: docker, т.к. внутри много разных компонентов и зависимостей, упаковка в контейнер в данном случае очень удобна.

## Задача 3

- Запустите первый контейнер из образа ***centos*** c любым тэгом в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Запустите второй контейнер из образа ***debian*** в фоновом режиме, подключив папку ```/data``` из текущей рабочей директории на хостовой машине в ```/data``` контейнера;
- Подключитесь к первому контейнеру с помощью ```docker exec``` и создайте текстовый файл любого содержания в ```/data```;
- Добавьте еще один файл в папку ```/data``` на хостовой машине;
- Подключитесь во второй контейнер и отобразите листинг и содержание файлов в ```/data``` контейнера.

Ответ:
```
Evgeniy@192 05-virt-03-docker % docker run --rm -it -d --name centos -v ~/Projects/netology/devops-netology/homeWorks/05-virt-03-docker/data:/data arm64v8/centos:latest
979fd5ea97a282de467be030f6b2b4d94d7e4c46135a53f960d7526fdd6c91ee
Evgeniy@192 05-virt-03-docker % docker run --rm -it -d --name debian -v ~/Projects/netology/devops-netology/homeWorks/05-virt-03-docker/data:/data arm64v8/debian:latest
3a3c4c90356a496a85b046bdf1cd2763467e9cd9fb58068b21472efefad0b184
Evgeniy@192 05-virt-03-docker % docker ps
CONTAINER ID   IMAGE                   COMMAND       CREATED          STATUS          PORTS     NAMES
3a3c4c90356a   arm64v8/debian:latest   "bash"        9 seconds ago    Up 8 seconds              debian
979fd5ea97a2   arm64v8/centos:latest   "/bin/bash"   30 seconds ago   Up 29 seconds             centos
Evgeniy@192 05-virt-03-docker % docker exec -it centos bash
[root@979fd5ea97a2 /]# touch data/test-centos.txt
[root@979fd5ea97a2 /]# ^C
[root@979fd5ea97a2 /]# exit
Evgeniy@192 05-virt-03-docker % touch data/test-local.txt
Evgeniy@192 05-virt-03-docker % docker exec -it debian bash
root@3a3c4c90356a:/# ls data/
test-centos.txt  test-local.txt
root@3a3c4c90356a:/# 
```
