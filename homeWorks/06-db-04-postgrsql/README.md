# Домашнее задание к занятию "6.4. PostgreSQL"

## Задача 1

Используя docker поднимите инстанс PostgreSQL (версию 13). Данные БД сохраните в volume.

Подключитесь к БД PostgreSQL используя `psql`.

Воспользуйтесь командой `\?` для вывода подсказки по имеющимся в `psql` управляющим командам.

**Найдите и приведите** управляющие команды для:
- вывода списка БД
- подключения к БД
- вывода списка таблиц
- вывода описания содержимого таблиц
- выхода из psql

### Ответ:
1. ```docker-compose up -d```
2. ```docker-compose exec db_postgres sh```
3. ```createdb --username=admin test_db```
4. ```psql --username=admin --dbname=test_db```
5. ```\?```
```
\l[+]   [PATTERN]      list databases
\c[onnect] {[DBNAME|- USER|- HOST|- PORT|-] | conninfo
\dt[S+] [PATTERN]      list tables
\d[S+]  NAME           describe table, view, sequence, or index
\q                     quit psql
```

## Задача 2

Используя `psql` создайте БД `test_database`.

Изучите [бэкап БД](https://github.com/netology-code/virt-homeworks/tree/virt-11/06-db-04-postgresql/test_data).

Восстановите бэкап БД в `test_database`.

Перейдите в управляющую консоль `psql` внутри контейнера.

Подключитесь к восстановленной БД и проведите операцию ANALYZE для сбора статистики по таблице.

Используя таблицу [pg_stats](https://postgrespro.ru/docs/postgresql/12/view-pg-stats), найдите столбец таблицы `orders` 
с наибольшим средним значением размера элементов в байтах.

**Приведите в ответе** команду, которую вы использовали для вычисления и полученный результат.

### Ответ:

Поднимаем контейер
```
docker-compose up -d
```

Заходим в контейнер
```
docker-compose exec db_postgres sh
```

Создаём новую DB test_database
```
createdb --username=admin test_database
```

Подключаемся к новой БД
```
psql --username=admin --dbname=test_database
```

Создаём нового пользователя с именем из приложенного в задании дампа, без него не получится применить дамп и выдаём ему права на БД.
```
CREATE USER "postgres" WITH PASSWORD 'passwd';
GRANT ALL PRIVILEGES ON DATABASE "test_database" to "postgres";
\q
```

Применяем дамп
```
psql --username=admin --dbname=test_database < /opt/test_data/test_dump.sql
```

Проверяем dump
```
psql --username=admin --dbname=test_database

\dt
         List of relations
 Schema |  Name  | Type  |  Owner   
--------+--------+-------+----------
 public | orders | table | postgres
(1 row)

\d orders
                                   Table "public.orders"
 Column |         Type          | Collation | Nullable |              Default               
--------+-----------------------+-----------+----------+------------------------------------
 id     | integer               |           | not null | nextval('orders_id_seq'::regclass)
 title  | character varying(80) |           | not null | 
 price  | integer               |           |          | 0
Indexes:
    "orders_pkey" PRIMARY KEY, btree (id)


select * from orders;
 id |        title         | price 
----+----------------------+-------
  1 | War and peace        |   100
  2 | My little database   |   500
  3 | Adventure psql time  |   300
  4 | Server gravity falls |   300
  5 | Log gossips          |   123
  6 | WAL never lies       |   900
  7 | Me and my bash-pet   |   499
  8 | Dbiezdmin            |   501
(8 rows)
```

Выполняем ANALYZE:
```
ANALYZE VERBOSE orders;

INFO:  analyzing "public.orders"
INFO:  "orders": scanned 1 of 1 pages, containing 8 live rows and 0 dead rows; 8 rows in sample, 8 estimated total rows
ANALYZE
```

Вывод статистики, искомый столбец `title`
```
select tablename, attname, avg_width from pg_stats where tablename = 'orders';
 tablename | attname | avg_width 
-----------+---------+-----------
 orders    | id      |         4
 orders    | title   |        16
 orders    | price   |         4

```

## Задача 3

Архитектор и администратор БД выяснили, что ваша таблица orders разрослась до невиданных размеров и
поиск по ней занимает долгое время. Вам, как успешному выпускнику курсов DevOps в нетологии предложили
провести разбиение таблицы на 2 (шардировать на orders_1 - price>499 и orders_2 - price<=499).

Предложите SQL-транзакцию для проведения данной операции.

Можно ли было изначально исключить "ручное" разбиение при проектировании таблицы orders?

### Ответ:
Т.к. таблица уже наполнена данными используем процедуру партиционирования через наследование.

Создаём таблицы-партиции:
```
CREATE TABLE orders_1 (
    CONSTRAINT primary_key_orders_1 primary key (id),
) INHERITS (orders);

CREATE TABLE orders_2 (
    CONSTRAINT primary_key_orders_2 primary key (id),
) INHERITS (orders);
```

Создаём функцию, обеспечивающую партицирование:
```
CREATE OR REPLACE FUNCTION     
    orders_insert_trigger()
RETURNS TRIGGER AS $$
BEGIN
IF ( NEW.price > 499 ) THEN    
        INSERT INTO orders_1 VALUES (NEW.*);
ELSIF ( NEW.price <= 499 ) THEN    
        INSERT INTO orders_2 VALUES (NEW.*);
ELSE
    RAISE EXCEPTION 'Date out of range.   
        Fix the orders_insert_trigger() function!';
END IF;
RETURN NULL;
END;
$$
LANGUAGE plpgsql;
```

Подключаем функцию к мастер-таблице:
```
CREATE TRIGGER insert_orders    
    BEFORE INSERT ON orders
    FOR EACH ROW EXECUTE FUNCTION orders_insert_trigger();
```

Правильное партиционирование при проектировании таблицы:
```
CREATE TABLE orders (
	id integer NOT NULL,
	title character varying(80) NOT NULL,
	price integer DEFAULT 0,
	CONSTRAINT orders_primary_key PRIMARY KEY (id)
) PARTITION BY RANGE (price);

CREATE TABLE orders_1 PARTITION OF orders
    FOR VALUES FROM (500) TO (maxvalue);
    
CREATE TABLE orders_2 PARTITION OF orders
    FOR VALUES FROM (minvalue) to (500);
```

## Задача 4

Используя утилиту `pg_dump` создайте бекап БД `test_database`.

Как бы вы доработали бэкап-файл, чтобы добавить уникальность значения столбца `title` для таблиц `test_database`?

### Ответ:

Создаём dump test_database
```
docker-compose exec db_postgres sh
pg_dump --username=admin --dbname=test_database > /opt/test_data/dump_test_database.sql
```

Дописываем альтер на уникальность в конец дампа:
```
echo "ALTER TABLE orders ADD CONSTRAIN orders_tilte_unique unique (title);" >> /opt/test_data/dump_test_database.sql
```

---

