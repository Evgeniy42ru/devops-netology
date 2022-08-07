
# Домашнее задание к занятию ["5.2. Применение принципов IaaC в работе с виртуальными машинами"](https://github.com/netology-code/virt-homeworks/tree/virt-11/05-virt-02-iaac)

## Задача 1

- Опишите своими словами основные преимущества применения на практике IaaC паттернов.
- Какой из принципов IaaC является основополагающим?

> Ответ:  
>1. Единая конфигурация, быстро вносить изменения, избегаем ошибок "ручной настройки".
>2. Скорость, экономия времени и ресурсов на разворот и маштабирование.
>3. Идемпотентность - является основополагающим принципом IaaC. Мы уверенны что при разворачивании инфраструктуры мы каждый раз будем получать ту же самую инфраструктуру с теми же настройками.


## Задача 2

- Чем Ansible выгодно отличается от других систем управление конфигурациями?
- Какой, на ваш взгляд, метод работы систем конфигурации более надёжный push или pull?

> Ответ:
>- Ansible использует готовую ssh инфраструктуру, не требует дополнительного по для взаимодействия с целевыми машинами.
>- Push, т.к. от одного ко многим. Гораздо проще контролировать процесс изменения и нактывания конфигурации. 


## Задача 3

Установить на личный компьютер:

- VirtualBox
```
evgeniy@r2-d2:~/projects/devops-netology/vagrant$ VBoxManage -v
6.1.32r149290
```
- Vagrant
```
evgeniy@r2-d2:~/projects/devops-netology/vagrant$ ./vagrant -v
Vagrant 2.2.19
```
- Ansible
```
evgeniy@r2-d2:~/projects/devops-netology/vagrant$ ansible --version
ansible 2.9.6
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/evgeniy/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/lib/python3/dist-packages/ansible
  executable location = /usr/bin/ansible
  python version = 3.8.10 (default, Mar 15 2022, 12:22:08) [GCC 9.4.0]
```
