# [Домашнее задание к занятию 4 «Работа с roles»](https://github.com/netology-code/mnt-homeworks/blob/MNT-video/08-ansible-04-role/README.md)

## Подготовка к выполнению

>1. * Необязательно. Познакомьтесь с [LightHouse](https://youtu.be/ymlrNlaHzIY?t=929).
>2. Создайте два пустых публичных репозитория в любом своём проекте: vector-role и lighthouse-role.
- https://github.com/Evgeniy42ru/lighthouse-role
- https://github.com/Evgeniy42ru/vector-role
>3. Добавьте публичную часть своего ключа к своему профилю на GitHub.

Добавил.

## Основная часть

Ваша цель — разбить ваш playbook на отдельные roles. 

Задача — сделать roles для ClickHouse, Vector и LightHouse и написать playbook для использования этих ролей. 

Ожидаемый результат — существуют три ваших репозитория: два с roles и один с playbook.

**Что нужно сделать**

>1. Создайте в старой версии playbook файл `requirements.yml` и заполните его содержимым:

   ```yaml
   ---
     - src: git@github.com:AlexeySetevoi/ansible-clickhouse.git
       scm: git
       version: "1.11.0"
       name: clickhouse 
   ```
[`requirements.yml`](./playbook/requirements.yml)

>2. При помощи `ansible-galaxy` скачайте себе эту роль.

```shell
ansible-galaxy install -r requirements.yml -p roles
Starting galaxy role install process
- extracting clickhouse to /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-04-role/playbook/roles/clickhouse
- clickhouse (1.11.0) was installed successfully
```

>3. Создайте новый каталог с ролью при помощи `ansible-galaxy role init vector-role`.

```shell
ansible-galaxy role init vector-role
- Role vector-role was created successfully
ansible-galaxy role init lighthouse-role
- Role lighthouse-role was created successfully
```

>4. На основе tasks из старого playbook заполните новую role. Разнесите переменные между `vars` и `default`.
- [`Vector`](./roles/vector-role/)
- [`Lighthouse`](./roles/lighthouse-role/)

>5. Перенести нужные шаблоны конфигов в `templates`.
- [`Vector`](./roles/vector-role/templates/)
- [`Lighthouse`](./roles/lighthouse-role/templates/)

>6. Опишите в `README.md` обе роли и их параметры.
- [`Vector`](./roles/vector-role/README.md)
- [`Lighthouse`](./roles/lighthouse-role/README.md)

>7. Повторите шаги 3–6 для LightHouse. Помните, что одна роль должна настраивать один продукт.

Повторил.

>8. Выложите все roles в репозитории. Проставьте теги, используя семантическую нумерацию. Добавьте roles в `requirements.yml` в playbook.

Выкладываю Lighthouse и проставляю тег.
```shell
git init
Initialized empty Git repository in /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-04-role/roles/lighthouse/.git/
git remote add origin https://github.com/Evgeniy42ru/lighthouse-role.git
git add .
git commit -m "Lighthouse role"
[main (root-commit) e642829] Lighthouse role
 8 files changed, 161 insertions(+)
 create mode 100644 README.md
 create mode 100644 defaults/main.yml
 create mode 100644 handlers/main.yml
 create mode 100644 meta/main.yml
 create mode 100644 tasks/main.yml
 create mode 100644 tests/inventory
 create mode 100644 tests/test.yml
 create mode 100644 vars/main.yml
git push --set-upstream origin main
Enumerating objects: 16, done.
Counting objects: 100% (16/16), done.
Delta compression using up to 8 threads
Compressing objects: 100% (9/9), done.
Writing objects: 100% (16/16), 2.54 KiB | 236.00 KiB/s, done.
Total 16 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/Evgeniy42ru/lighthouse-role.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

git tag  
lighthouse-role % git tag 1.0.0         
lighthouse-role % git push origin --tags
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/Evgeniy42ru/lighthouse-role.git
 * [new tag]         1.0.0 -> 1.0.0
```

Выкладываю Vector и проставляю тег.
```shell
git init
Initialized empty Git repository in /Users/Evgeniy/Projects/netology/devops-netology/homeWorks/08-ansible-04-role/roles/vector-role/.git/
vector-role % git remote add origin https://github.com/Evgeniy42ru/vector-role.git
vector-role % git add .
vector-role % git commit -m "Vector role"
[main (root-commit) c683d3b] Vector role
 9 files changed, 113 insertions(+)
 create mode 100644 README.md
 create mode 100644 defaults/main.yml
 create mode 100644 handlers/main.yml
 create mode 100644 meta/main.yml
 create mode 100644 tasks/main.yml
 create mode 100644 templates/vector/vector.toml.j2
 create mode 100644 tests/inventory
 create mode 100644 tests/test.yml
 create mode 100644 vars/main.yml
vector-role % git commit -m "Vector role"
vector-role % git push --set-upstream origin main
Enumerating objects: 19, done.
Counting objects: 100% (19/19), done.
Delta compression using up to 8 threads
Compressing objects: 100% (8/8), done.
Writing objects: 100% (19/19), 2.34 KiB | 343.00 KiB/s, done.
Total 19 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/Evgeniy42ru/vector-role.git
 * [new branch]      main -> main
branch 'main' set up to track 'origin/main'.

git tag 1.0.0                      
vector-role % git push origin --tags
Total 0 (delta 0), reused 0 (delta 0), pack-reused 0
To https://github.com/Evgeniy42ru/vector-role.git
 * [new tag]         1.0.0 -> 1.0.0
```

Добавил roles в `requirements.yml` в playbook.
[`requirements.yml`](./playbook/requirements.yml)

>9. Переработайте playbook на использование roles. Не забудьте про зависимости LightHouse и возможности совмещения `roles` с `tasks`.

[`Переработайте playbook`](./playbook/site.yml)

>10. Выложите playbook в репозиторий.


11. В ответе дайте ссылки на оба репозитория с roles и одну ссылку на репозиторий с playbook.

---

### Как оформить решение задания

Выполненное домашнее задание пришлите в виде ссылки на .md-файл в вашем репозитории.

---