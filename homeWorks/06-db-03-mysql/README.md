# Домашнее задание к занятию ["6.3. MySQL"](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-03-mysql)

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс MySQL (версию 8). Данные БД сохраните в volume.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/master/06-db-03-mysql/test_data) и 
восстановитесь из него.

Перейдите в управляющую консоль `mysql` внутри контейнера.

Используя команду `\h` получите список управляющих команд.

Найдите команду для выдачи статуса БД и **приведите в ответе** из ее вывода версию сервера БД.

Подключитесь к восстановленной БД и получите список таблиц из этой БД.

**Приведите в ответе** количество записей с `price` > 300.

В следующих заданиях мы будем продолжать работу с данным контейнером.

### Ответ
```
docker-compose up -d

docker-compose exec mysql bash -c "mysql -uroot -ppasswd -e 'CREATE DATABASE test_db'" 

docker-compose exec mysql bash -c "mysql -uroot -ppasswd -Dtest_db < /opt/dump/test_dump.sql"

docker-compose exec mysql mysql -uroot -ppasswd

mysql> \status
--------------
mysql  Ver 8.0.30 for Linux on aarch64 (MySQL Community Server - GPL)

mysql> \u test_db
Reading table information for completion of table and column names
You can turn off this feature to get a quicker startup with -A

Database changed

mysql> SHOW TABLES;
+-------------------+
| Tables_in_test_db |
+-------------------+
| orders            |
+-------------------+
1 row in set (0.00 sec)

mysql> select count(id) from orders where price > 300;
+-----------+
| count(id) |
+-----------+
|         1 |
+-----------+
1 row in set (0.00 sec)

```

## Задача 2

Создайте пользователя test в БД c паролем test-pass, используя:
- плагин авторизации mysql_native_password
- срок истечения пароля - 180 дней 
- количество попыток авторизации - 3 
- максимальное количество запросов в час - 100
- аттрибуты пользователя:
    - Фамилия "Pretty"
    - Имя "James"

Предоставьте привелегии пользователю `test` на операции SELECT базы `test_db`.
    
Используя таблицу INFORMATION_SCHEMA.USER_ATTRIBUTES получите данные по пользователю `test` и 
**приведите в ответе к задаче**.

### Ответ
- https://dev.mysql.com/doc/refman/8.0/en/create-user.html

```
mysql> CREATE USER 'test' 
    ->   IDENTIFIED WITH mysql_native_password BY 'test-pass'
    ->   WITH MAX_QUERIES_PER_HOUR 100
    ->   PASSWORD EXPIRE INTERVAL 180 DAY
    ->   FAILED_LOGIN_ATTEMPTS 3
    ->   ATTRIBUTE '{"last_name": "Pretty", "first_name": "James"}';
Query OK, 0 rows affected (0.03 sec)

mysql> GRANT SELECT ON test_db.* TO 'test';
Query OK, 0 rows affected (0.01 sec)

select * from INFORMATION_SCHEMA.USER_ATTRIBUTES where USER like 'test';
+------+------+------------------------------------------------+
| USER | HOST | ATTRIBUTE                                      |
+------+------+------------------------------------------------+
| test | %    | {"last_name": "Pretty", "first_name": "James"} |
+------+------+------------------------------------------------+
1 row in set (0.01 sec)
```

## Задача 3

Установите профилирование `SET profiling = 1`.
Изучите вывод профилирования команд `SHOW PROFILES;`.

Исследуйте, какой `engine` используется в таблице БД `test_db` и **приведите в ответе**.

Измените `engine` и **приведите время выполнения и запрос на изменения из профайлера в ответе**:
- на `MyISAM`
- на `InnoDB`

### Ответ

- https://dev.mysql.com/doc/refman/8.0/en/show-profile.html

```
SET profiling = 1;
Query OK, 0 rows affected, 1 warning (0.00 sec)

mysql> SHOW PROFILES;
+----------+------------+----------------------+
| Query_ID | Duration   | Query                |
+----------+------------+----------------------+
|        4 | 0.00045050 | select * from orders |
|        5 | 0.00058850 | select * from orders |
|        6 | 0.00063025 | select * from orders |
|        7 | 0.00060075 | select * from orders |
|        8 | 0.00056150 | select * from orders |
|        9 | 0.00061275 | select * from orders |
|       10 | 0.00067600 | select * from orders |
|       11 | 0.00073925 | select * from orders |
|       12 | 0.00054325 | select * from orders |
|       13 | 0.00056475 | select * from orders |
|       14 | 0.00048275 | select * from orders |
|       15 | 0.00055325 | select * from orders |
|       16 | 0.00057650 | select * from orders |
|       17 | 0.00054075 | select * from orders |
|       18 | 0.00071950 | select * from orders |
+----------+------------+----------------------+
15 rows in set, 1 warning (0.00 sec)

mysql> select engine from INFORMATION_SCHEMA.TABLES where table_name like 'orders';
+--------+
| ENGINE |
+--------+
| InnoDB |
+--------+
1 row in set (0.01 sec)

mysql> select * from orders as query_InnoDB ;
+----+-----------------------+-------+
| id | title                 | price |
+----+-----------------------+-------+
|  1 | War and Peace         |   100 |
|  2 | My little pony        |   500 |
|  3 | Adventure mysql times |   300 |
|  4 | Server gravity falls  |   300 |
|  5 | Log gossips           |   123 |
+----+-----------------------+-------+
5 rows in set (0.00 sec)

mysql> alter table orders ENGINE='MYISAM';
Query OK, 5 rows affected (0.09 sec)
Records: 5  Duplicates: 0  Warnings: 0

mysql> select * from orders as query_MYISAM ;
+----+-----------------------+-------+
| id | title                 | price |
+----+-----------------------+-------+
|  1 | War and Peace         |   100 |
|  2 | My little pony        |   500 |
|  3 | Adventure mysql times |   300 |
|  4 | Server gravity falls  |   300 |
|  5 | Log gossips           |   123 |
+----+-----------------------+-------+
5 rows in set (0.00 sec)

mysql> SHOW PROFILES;
+----------+------------+-----------------------------------------------------------------------------+
| Query_ID | Duration   | Query                                                                       |
+----------+------------+-----------------------------------------------------------------------------+
|       19 | 0.01344175 | select engine from INFORMATION_SCHEMA.TABLES where table_name like 'orders' |
|       20 | 0.00051925 | select * from orders as query_InnoDB                                        |
|       21 | 0.08934025 | alter table orders ENGINE='MYISAM'                                          |
|       22 | 0.00103325 | select * from orders as query_MYISAM                                        |
+----------+------------+-----------------------------------------------------------------------------+
15 rows in set, 1 warning (0.00 sec)

mysql> alter table orders ENGINE='InnoDB';
Query OK, 5 rows affected (0.05 sec)
Records: 5  Duplicates: 0  Warnings: 0
```

## Задача 4 

Изучите файл `my.cnf` в директории /etc/mysql.

Измените его согласно ТЗ (движок InnoDB):
- Скорость IO важнее сохранности данных
- Нужна компрессия таблиц для экономии места на диске
- Размер буффера с незакомиченными транзакциями 1 Мб
- Буффер кеширования 30% от ОЗУ
- Размер файла логов операций 100 Мб

Приведите в ответе измененный файл `my.cnf`.

### Ответ:
- https://dev.mysql.com/doc/refman/8.0/en/innodb-configuration.html
- https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html

### Скорость IO важнее сохранности данных
- `innodb_flush_log_at_trx_commit = 2`

### Размер буффера с незакомиченными транзакциями 1 Мб
- The minimum innodb_log_file_size is 4MB.
- https://dev.mysql.com/doc/refman/8.0/en/innodb-parameters.html#sysvar_innodb_log_file_size
- `innodb_log_file_size=4MB`

### Буффер кеширования 30% от ОЗУ, предположим у нас 8gb на сервере.
- `innodb_buffer_pool_size=3221225472`

### Размер файла логов операций 100 Мб
- `max_binlog_size=104857600`
