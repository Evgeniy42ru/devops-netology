# Домашнее задание к занятию ["6.2. SQL"](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-02-sql)

## Введение

Перед выполнением задания вы можете ознакомиться с 
[дополнительными материалами](https://github.com/netology-code/virt-homeworks/tree/master/additional/README.md).

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 12) c 2 volume, 
в который будут складываться данные БД и бэкапы.

Приведите получившуюся команду или docker-compose манифест.

### Ответ:

1. docker-compose up -d


## Задача 2

В БД из задачи 1: 
- создайте пользователя test-admin-user и БД test_db
- в БД test_db создайте таблицу orders и clients (спeцификация таблиц ниже)
- предоставьте привилегии на все операции пользователю test-admin-user на таблицы БД test_db
- создайте пользователя test-simple-user  
- предоставьте пользователю test-simple-user права на SELECT/INSERT/UPDATE/DELETE данных таблиц БД test_db

Таблица orders:
- id (serial primary key)
- наименование (string)
- цена (integer)

Таблица clients:
- id (serial primary key)
- фамилия (string)
- страна проживания (string, index)
- заказ (foreign key orders)

Приведите:
- итоговый список БД после выполнения пунктов выше,
- описание таблиц (describe)
- SQL-запрос для выдачи списка пользователей с правами над таблицами test_db
- список пользователей с правами над таблицами test_db

### Ответ

2. docker-compose exec db_postgres sh
3. createdb --username=admin test_db
4. docker-compose exec db_postgres psql --username=admin --dbname=test_db
- CREATE USER "test-admin-user" WITH PASSWORD 'passwd';
5. CREATE TABLE orders (id serial primary key, наименование string, цена integer); (ERROR:  type "string" does not exist)
6. CREATE TABLE orders (id serial primary key, наименование varchar, цена integer);
7. CREATE TABLE clients (id serial primary key, фамилия varchar, "страна проживания" varchar index, заказ foreign key orders); (ERROR:  syntax error at or near "index")
8. CREATE TABLE clients (id serial primary key, фамилия varchar, "страна проживания" varchar, заказ integer CONSTRAINT fk_orders REFERENCES orders(id));
!!! кирилица в именах столбцов, пробелы. Не надо так.
9. 
```
test_db=# \l
 admin     | admin | UTF8     | en_US.utf8 | en_US.utf8 | 
 postgres  | admin | UTF8     | en_US.utf8 | en_US.utf8 | 
 template0 | admin | UTF8     | en_US.utf8 | en_US.utf8 | =c/admin         +
           |       |          |            |            | admin=CTc/admin
 template1 | admin | UTF8     | en_US.utf8 | en_US.utf8 | =c/admin         +
           |       |          |            |            | admin=CTc/admin
 test_db   | admin | UTF8     | en_US.utf8 | en_US.utf8 | 

test_db=# \dt
 public | clients | table | admin
 public | orders  | table | admin

test_db=# \d orders
                                    Table "public.orders"
    Column    |       Type        | Collation | Nullable |              Default               
--------------+-------------------+-----------+----------+------------------------------------
 id           | integer           |           | not null | nextval('orders_id_seq'::regclass)
 наименование | character varying |           |          | 
 цена         | integer           |           |          | 
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)
Referenced by:
    TABLE "clients" CONSTRAINT "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)

test_db=# \d clients
                                       Table "public.clients"
      Column       |       Type        | Collation | Nullable |               Default               
-------------------+-------------------+-----------+----------+-------------------------------------
 id                | integer           |           | not null | nextval('clients_id_seq'::regclass)
 фамилия           | character varying |           |          | 
 страна проживания | character varying |           |          | 
 заказ             | integer           |           |          | 
Indexes:
    "clients_pkey" PRIMARY KEY, btree (id)
Foreign-key constraints:
    "fk_orders" FOREIGN KEY ("заказ") REFERENCES orders(id)

```

10. GRANT ALL PRIVILEGES ON DATABASE "test_db" to "test-admin-user";
11. CREATE USER "test-simple-user" WITH PASSWORD 'passwd';
12. REVOKE ALL ON DATABASE "test_db" from "test-simple-user";
13. GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA "public" to "test-simple-user";

12. SELECT table_schema, table_catalog, table_name, grantee, privilege_type FROM information_schema.table_privileges WHERE table_catalog like 'test_db';
13. SELECT DISTINCT grantee FROM information_schema.table_privileges WHERE table_catalog like 'test_db' group by grantee;
 PUBLIC
 admin
 test-simple-user

## Задача 3

Используя SQL синтаксис - наполните таблицы следующими тестовыми данными:

Таблица orders

|Наименование|цена|
|------------|----|
|Шоколад| 10 |
|Принтер| 3000 |
|Книга| 500 |
|Монитор| 7000|
|Гитара| 4000|

Таблица clients

|ФИО|Страна проживания|
|------------|----|
|Иванов Иван Иванович| USA |
|Петров Петр Петрович| Canada |
|Иоганн Себастьян Бах| Japan |
|Ронни Джеймс Дио| Russia|
|Ritchie Blackmore| Russia|

Используя SQL синтаксис:
- вычислите количество записей для каждой таблицы 
- приведите в ответе:
    - запросы 
    - результаты их выполнения.

### Ответ
```
insert into orders (наименование, цена) values
    ('Шоколад', 10),
    ('Принтер', 3000),
    ('Книга', 500),
    ('Монитор', 7000),
    ('Гитара', 4000); 
INSERT 0 5

select * from orders;
  1 | Шоколад      |   10
  2 | Принтер      | 3000
  3 | Книга        |  500
  4 | Монитор      | 7000
  5 | Гитара       | 4000

insert into clients (фамилия, "страна проживания") values
    ('Иванов Иван Иванович', 'USA'),
    ('Петров Петр Петрович', 'Canada'),
    ('Иоганн Себастьян Бах', 'Japan'),
    ('Ронни Джеймс Дио', 'Russia'),
    ('Ritchie Blackmore', 'Russia');
INSERT 0 5

test_db=# select * from clients;
  1 | Иванов Иван Иванович | USA               |      
  2 | Петров Петр Петрович | Canada            |      
  3 | Иоганн Себастьян Бах | Japan             |      
  4 | Ронни Джеймс Дио     | Russia            |      
  5 | Ritchie Blackmore    | Russia            |  

test_db=# select count(id) from orders;
     5

test_db=# select count(id) from clients;
     5

```

## Задача 4

Часть пользователей из таблицы clients решили оформить заказы из таблицы orders.

Используя foreign keys свяжите записи из таблиц, согласно таблице:

|ФИО|Заказ|
|------------|----|
|Иванов Иван Иванович| Книга |
|Петров Петр Петрович| Монитор |
|Иоганн Себастьян Бах| Гитара |

Приведите SQL-запросы для выполнения данных операций.

Приведите SQL-запрос для выдачи всех пользователей, которые совершили заказ, а также вывод данного запроса.
 
Подсказк - используйте директиву `UPDATE`.

### Ответ
```
update clients
set "заказ" = (
    select id
    from orders
    where orders."наименование" = 'Книга'
) 
where clients."фамилия" = 'Иванов Иван Иванович';

update clients
set "заказ" = (
    select id
    from orders
    where orders."наименование" = 'Монитор'
) 
where clients."фамилия" = 'Петров Петр Петрович';

update clients
set "заказ" = (
    select id
    from orders
    where orders."наименование" = 'Гитара'
) 
where clients."фамилия" = 'Иоганн Себастьян Бах';

select * from clients join orders on clients.id = orders.id where clients."заказ" is not null; 
  1 | Иванов Иван Иванович | USA               |     3 |  1 | Шоколад      |   10
  2 | Петров Петр Петрович | Canada            |     4 |  2 | Принтер      | 3000
  3 | Иоганн Себастьян Бах | Japan             |     5 |  3 | Книга        |  500

```

## Задача 5

Получите полную информацию по выполнению запроса выдачи всех пользователей из задачи 4 
(используя директиву EXPLAIN).

Приведите получившийся результат и объясните что значат полученные значения.

```
EXPLAIN select * from clients join orders on clients.id = orders.id where clients."заказ" is not null;
 Hash Join  (cost=28.18..53.34 rows=806 width=112)
   Hash Cond: (orders.id = clients.id)
   ->  Seq Scan on orders  (cost=0.00..22.00 rows=1200 width=40)
   ->  Hash  (cost=18.10..18.10 rows=806 width=72)
         ->  Seq Scan on clients  (cost=0.00..18.10 rows=806 width=72)
               Filter: ("заказ" IS NOT NULL)

- Hash Join начинает работу с того, что обращается к дочернему узлу Hash. Тот получает от своего дочернего узла (здесь SeqScan весь набор строк и строит хеш-таблицу.
- Затем Hash Join обращается ко второму дочернему узлу и соединяет строки, постепенно возвращая полученные результаты.
- cost - приблизительная стоимость запроса.
- rows - ожидаемое число строк.
- width - ожидаемый средний размер строк.
- filter - условия на возвращаемый результат.
```

## Задача 6

Создайте бэкап БД test_db и поместите его в volume, предназначенный для бэкапов (см. Задачу 1).

Остановите контейнер с PostgreSQL (но не удаляйте volumes).

Поднимите новый пустой контейнер с PostgreSQL.

Восстановите БД test_db в новом контейнере.

Приведите список операций, который вы применяли для бэкапа данных и восстановления. 

### Ответ
```
docker-compose exec db_postgres pg_dump -U admin -d test_db > /opt/test_db_dump.sql

docker-compose up -d
Starting 06-db-02-sql_db_postgres_1  ... done
Creating 06-db-02-sql_db3_postgres_1 ... done
docker-compose exec db3_postgres psql --username=admin --dbname=test_db
psql: error: connection to server on socket "/var/run/postgresql/.s.PGSQL.5432" failed: FATAL:  database "test_db" does not exist

docker-compose exec db_postgres createdb --username=admin test_db      
createdb: error: database creation failed: ERROR:  database "test_db" already exists

docker-compose exec db3_postgres createdb --username=admin test_db
docker-compose exec db3_postgres sh
psql --username=admin --dbname=test_db < /opt/test_db_dump.sql  
psql --username=admin --dbname=test_db
test_db=# \dt
        List of relations
 Schema |  Name   | Type  | Owner 
--------+---------+-------+-------
 public | clients | table | admin
 public | orders  | table | admin
(2 rows)

```

---
