# Домашнее задание к занятию [«Базовые объекты K8S»](https://github.com/netology-code/kuber-homeworks/blob/main/1.2/1.2.md)

### Цель задания

В тестовой среде для работы с Kubernetes, установленной в предыдущем ДЗ, необходимо развернуть Pod с приложением и подключиться к нему со своего локального компьютера. 

------

### Чеклист готовности к домашнему заданию

1. Установленное k8s-решение (например, MicroK8S).
2. Установленный локальный kubectl.
3. Редактор YAML-файлов с подключенным Git-репозиторием.

------

### Инструменты и дополнительные материалы, которые пригодятся для выполнения задания

1. Описание [Pod](https://kubernetes.io/docs/concepts/workloads/pods/) и примеры манифестов.
2. Описание [Service](https://kubernetes.io/docs/concepts/services-networking/service/).

------

### Задание 1. Создать Pod с именем hello-world

1. Создать манифест (yaml-конфигурацию) Pod.
2. Использовать image - gcr.io/kubernetes-e2e-test-images/echoserver:2.2.
3. Подключиться локально к Pod с помощью `kubectl port-forward` и вывести значение (curl или в браузере).

------

### Задание 2. Создать Service и подключить его к Pod

1. Создать Pod с именем netology-web.
2. Использовать image — gcr.io/kubernetes-e2e-test-images/echoserver:2.2.
3. Создать Service с именем netology-svc и подключить к netology-web.
4. Подключиться локально к Service с помощью `kubectl port-forward` и вывести значение (curl или в браузере).

------

### Правила приёма работы

1. Домашняя работа оформляется в своем Git-репозитории в файле README.md. Выполненное домашнее задание пришлите ссылкой на .md-файл в вашем репозитории.
2. Файл README.md должен содержать скриншоты вывода команд `kubectl get pods`, а также скриншот результата подключения.
3. Репозиторий должен содержать файлы манифестов и ссылки на них в файле README.md.

------

### Критерии оценки
Зачёт — выполнены все задания, ответы даны в развернутой форме, приложены соответствующие скриншоты и файлы проекта, в выполненных заданиях нет противоречий и нарушения логики.

На доработку — задание выполнено частично или не выполнено, в логике выполнения заданий есть противоречия, существенные недостатки.

------

## Решение

### Задание 1. Создать Pod с именем hello-world

1. Использую VM из прошлого задания с установленнным `MicroK8S`
2. Т.к. VM прерываемая, при повторном зауске изменился IP, повторил шаги с добавлением IP в конфиг, генерацией новых сертификатов и экспортом настроек на локальный `kubectl` для подключения.
3. Создал манифест - [pod-hello-world.yml](./config/pod-hello-world.yml)
4. Применяем манифест 
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl apply -f ~/Projects/netology/devops-netology/homeWorks/12-kuber-homeworks/12.2/config/pod-hello-world.yml
pod/hello-world created

Evgeniy@Evgenijs-MacBook-Pro ~ %  kubectl get pods
NAME         READY   STATUS    RESTARTS   AGE
echoserver   1/1     Running   0          5m55s
```
5. Включаем проброс портов
```shell
evgeniy@microk8s:~$ microk8s kubectl port-forward echoserver 30080:80
Forwarding from 127.0.0.1:30080 -> 80
Forwarding from [::1]:30080 -> 80
```
6. Делаем запрос
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % curl 158.160.84.113:30080
curl: (52) Empty reply from server
```
Проброс отваливается.
```
evgeniy@microk8s:~$ microk8s kubectl port-forward -n default echoserver 30080:80 --address='0.0.0.0'
Forwarding from 0.0.0.0:30080 -> 80
Handling connection for 30080
E1112 17:41:48.723624  258370 portforward.go:409] an error occurred forwarding 30080 -> 80: error forwarding port 80 to pod c353599ce53b5bdd85fa23a93c1fd3f858be75a95dfe0d2956ce7ed1cee4c2b3, uid : failed to execute portforward in network namespace "/var/run/netns/cni-742d1a4e-4966-9085-47a1-fae6be80bc99": failed to connect to localhost:80 inside namespace "c353599ce53b5bdd85fa23a93c1fd3f858be75a95dfe0d2956ce7ed1cee4c2b3", IPv4: dial tcp4 127.0.0.1:80: connect: connection refused IPv6 dial tcp6 [::1]:80: connect: connection refused
error: lost connection to pod
```

Искал причину, основная причина данной ситуации если порт занят чем то ещё. В моей ситуации 1 pod, порт свободен. Пробовал перезапускать `microk8s`, удалять pod - не помогает, с данным образом проброс не работает. Решил проверить с образом nginx.

7. Делаю манифест под [nginx](./config/pod-nginx.yml), использую VM из прошлого задания с установленнным `MicroK8S`, т.к. VM прерываемая IP изменился. Прописываю новый внешний IP в конфиг `MicroK8S`, обновляю сертификаты. Прописываю новые креды в локальный конфиг `kubectl`.

8. Применяю манифест [nginx](./config/pod-nginx.yml)
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl apply -f ~/Projects/netology/devops-netology/homeWorks/12-kuber-homeworks/12.2/config/pod-nginx.yml
pod/nginx created
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl get pods                                                                                           
NAME    READY   STATUS              RESTARTS   AGE
nginx   0/1     ContainerCreating   0          3s
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl get pods 
NAME    READY   STATUS              RESTARTS   AGE
nginx   0/1     ContainerCreating   0          6s
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl get pods 
NAME    READY   STATUS    RESTARTS   AGE
nginx   1/1     Running   0          13s
```
9. Включаю проброс портов
```shell
evgeniy@microk8s:~$ microk8s kubectl port-forward nginx 30080:80 --address='0.0.0.0'
Forwarding from 0.0.0.0:30080 -> 80
```

10. Делаю запрос с локальной машины
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % curl 158.160.74.243:30080         
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
    body {
        width: 35em;
        margin: 0 auto;
        font-family: Tahoma, Verdana, Arial, sans-serif;
    }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

### Задание 2. Создать Service и подключить его к Pod

1. Сделал [манифест](./config/netology-web.yml) содержащий Pod с именем netology-web и Service с именем netology-svc, image "gcr.io/kubernetes-e2e-test-images/echoserver:2.2" не использую, причину описал в 1 задании.

2. Применяю [манифест](./config/netology-web.yml)
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl apply -f ~/Projects/netology/devops-netology/homeWorks/12-kuber-homeworks/12.2/config/netology-web.yml
```![Alt text](curl.png) ![Alt text](get_pods.png)

Проверяю:
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % kubectl get nodes && kubectl get svc && kubectl get pods
NAME       STATUS   ROLES    AGE   VERSION
microk8s   Ready    <none>   20h   v1.27.7
NAME           TYPE        CLUSTER-IP       EXTERNAL-IP   PORT(S)   AGE
kubernetes     ClusterIP   10.152.183.1     <none>        443/TCP   20h
netology-svc   ClusterIP   10.152.183.249   <none>        80/TCP    12m
NAME           READY   STATUS    RESTARTS      AGE
hello-world    1/1     Running   2 (47m ago)   20h
nginx          1/1     Running   2 (47m ago)   20h
netology-web   1/1     Running   0             12m
```

3. Включаю проброс портов
```shell
evgeniy@microk8s:~$ microk8s kubectl port-forward svc/netology-svc 30080:80 --address='0.0.0.0'
Forwarding from 0.0.0.0:30080 -> 80
```

4. Делаю запрос с локальной машины
```shell
Evgeniy@Evgenijs-MacBook-Pro ~ % curl 158.160.74.243:30080                                                                                     
<!DOCTYPE html>
<html>
<head>
<title>Welcome to nginx!</title>
<style>
html { color-scheme: light dark; }
body { width: 35em; margin: 0 auto;
font-family: Tahoma, Verdana, Arial, sans-serif; }
</style>
</head>
<body>
<h1>Welcome to nginx!</h1>
<p>If you see this page, the nginx web server is successfully installed and
working. Further configuration is required.</p>

<p>For online documentation and support please refer to
<a href="http://nginx.org/">nginx.org</a>.<br/>
Commercial support is available at
<a href="http://nginx.com/">nginx.com</a>.</p>

<p><em>Thank you for using nginx.</em></p>
</body>
</html>
```

5. Скришоты:
![`kubectl get nodes && kubectl get svc && kubectl get pods`](./img/get_pods.png)
![`curl 158.160.74.243:30080`](./img/curl.png)