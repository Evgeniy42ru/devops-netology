# Домашнее задание к занятию ["5.5. Оркестрация кластером Docker контейнеров на примере Docker Swarm"](https://github.com/netology-code/virt-homeworks/tree/virt-11/05-virt-05-docker-swarm)

---

## Задача 1

Дайте письменые ответы на следующие вопросы:

- В чём отличие режимов работы сервисов в Docker Swarm кластере: replication и global?
> replication  
> - Кол-во поднятых сервисов зависит от числа которое мы указали в настройках.
> - Не зависит от числа нод.

> global
> - Кол-во сервисов зависит от кол-во нод.
> - Нельзя задавать кол-во в настройках, сервис поднимается на каждой ноде.
- Какой алгоритм выбора лидера используется в Docker Swarm кластере?
> Raft
- Что такое Overlay Network?
>Overlay-сети используются в контексте кластеров (Docker Swarm), где виртуальная сеть, которую используют контейнеры, связывает несколько физических хостов, на которых запущен Docker. Предоставляет доступ к контейнерам внутри сети по их имени.


## Задача 2

Создать ваш первый Docker Swarm кластер в Яндекс.Облаке

Для получения зачета, вам необходимо предоставить скриншот из терминала (консоли), с выводом команды:
```
docker node ls
```
### Ответ:
```
Ход выполнения:
1. terraform init - без впн не работает
2. terraform validate
3. terraform plan
4. terraform apply -auto-approve
5. ssh centos@51.250.79.168
6. sudo docker node ls
7. sudo docker service ls

[centos@node01 ~]$ sudo docker node ls
ID                            HOSTNAME             STATUS    AVAILABILITY   MANAGER STATUS   ENGINE VERSION
wdp0xt9g4m7eejx52ly36mvbl *   node01.netology.yc   Ready     Active         Leader           20.10.17
9zhy1xis37l2f51uwvdzga24l     node02.netology.yc   Ready     Active         Reachable        20.10.17
p6wl9mfgr9p6snnmn2z91l4nk     node03.netology.yc   Ready     Active         Reachable        20.10.17
9nqtbinfysas8rctdyatltqpt     node04.netology.yc   Ready     Active                          20.10.17
n6siymek1gbr80jok4rpc7juj     node05.netology.yc   Ready     Active                          20.10.17
u0shzux9mvcxdsregnbpvjaej     node06.netology.yc   Ready     Active                          20.10.17
```

## Задача 3

Создать ваш первый, готовый к боевой эксплуатации кластер мониторинга, состоящий из стека микросервисов.

Для получения зачета, вам необходимо предоставить скриншот из терминала (консоли), с выводом команды:
```
docker service ls
```

### Ответ:
```
[centos@node01 ~]$ sudo docker service ls
ID             NAME                                MODE         REPLICAS   IMAGE                                          PORTS
tzngrdx4z9ce   swarm_monitoring_alertmanager       replicated   1/1        stefanprodan/swarmprom-alertmanager:v0.14.0
iuejwbekn46b   swarm_monitoring_caddy              replicated   1/1        stefanprodan/caddy:latest                      *:3000->3000/tcp, *:9090->9090/tcp, *:9093-9094->9093-9094/tcp
ynoa54odoq0d   swarm_monitoring_cadvisor           global       6/6        google/cadvisor:latest
r7b6cttwfrzs   swarm_monitoring_dockerd-exporter   global       6/6        stefanprodan/caddy:latest
mklfsbcee307   swarm_monitoring_grafana            replicated   1/1        stefanprodan/swarmprom-grafana:5.3.4
okze0xyh7i3l   swarm_monitoring_node-exporter      global       6/6        stefanprodan/swarmprom-node-exporter:v0.16.0
jca82usho3o4   swarm_monitoring_prometheus         replicated   1/1        stefanprodan/swarmprom-prometheus:v2.5.0
wmuszft8rxfd   swarm_monitoring_unsee              replicated   1/1        cloudflare/unsee:v0.8.0
```

## Очищаем облако  
```
1. terraform destroy -auto-approve
2. yc compute image delete --id {{ image_id }}
```
