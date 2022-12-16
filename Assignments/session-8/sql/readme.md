## Create Connector to {Postgres}
```
ksql>
CREATE SOURCE CONNECTOR kdrm_source WITH (
    'connector.class'                           = 'io.debezium.connector.postgresql.PostgresConnector',
    'database.port'                             = '5432',
    'database.hostname'                         = 'postgres',
    'database.dbname'                           = 'db_postgres',
    'database.user'                             = 'postgres_u',
    'database.password'                         = 'postpass',
    'database.server.name'                      = 'db_postgres',
    'database.whitelist'                        = 'db_postgres',
    'topic.prefix'                              = 'psql_connect01',
    'table.include.list'                        = 'db_postgres.kdrama_list',
    'database.history.kafka.bootstrap.servers'  = 'broker:9092',
    'database.history.kafka.topic'              = 'schema-changes.db_postgres',
    'key.converter'                             = 'org.apache.kafka.connect.storage.StringConverter',
    'value.converter'                           = 'io.confluent.connect.avro.AvroConverter',
    'key.converter.schemas.enable'              = 'false',
    'value.converter.schemas.enable'            = 'true',
    'value.converter.schema.registry.url'       = 'http://schema-registry:8081'
);
```

## Create & Insert to Postgres Table
```
postgres=#
create table kdrama_list (
    list_id int primary key,
    drama_name varchar(150),
    episodes int,
    orig_network varchar(75),
    score_list float,
    scored_by int,
    watchers float,
    imdb_desc varchar(255)
    );
```

```
postgres=#
insert into kdrama_list values 
    (1, 'Move to Heaven', 10, 'Netflix', 9.2, 26058, 51979, 'Working as trauma cleaners, both Gu-ru and Sang-gu uncover various stories of the deceased while exp...'),
    (2, 'Extraordinary Attorney Woo', 16, 'Netflix', 9.2, 8535, 33699, 'About an autistic 27-year-old lawyer. Due to her high IQ of 164, impressive memory, and creative tho...'),
    (3, 'Hospital Playlist', 12, 'Netlix-TVN', 9.1, 32842, 72138, 'Hospital Playlist tells the story of five doctors who have been friends since they entered medical s...'),
    (4, 'Its Okay to Not be Okay', 16, 'Netflix-TVN', 9, 71704, 129299, 'An extraordinary road to emotional healing opens up for an selfish antisocial children s book writer...'),
    (5, 'Guardian: The Lonely and Great God - Goblin', 16, 'TVN', 8.8, 91993, 173027, 'In his quest for a bride to break his immortal curse, Dokkaebi, a 939-year-old guardian of souls, me...'),
    (6, 'Mouse', 20, 'TVN', 8.8, 13640, 37206, 'A suspenseful story that will center around the key question, What if we could sort out psychopaths...'),
    (7, 'Start Up', 16, 'Netflix-TVN', 8.1, 36309, 70484, 'Young entrepreneurs aspiring to launch virtual dreams into reality compete for success and love in t...'),
    (8, 'Descendants of the Sun', 16, 'KBS2', 8.7, 77045, 146812, 'This drama tells of the love story that develops between a surgeon and a special forces officer...'),
    (9, 'Dr Romantic', 20, 'SBS', 8.7, 22827, 48508, 'Romantic Doctor Kim is a real doctor story set in a small, humble hospital called Dol Dam Hospit...'),
    (10, 'Vincenzo', 20, 'Netflix-TVN', 9, 51495, 92974, 'During a visit to his motherland, a Korean-Italian mafia lawyer gives an unrivaled conglomerate a ta...');
```

## Create Stream & Empty Final Tabel on ksqlDB (ensure that kafka_topic listed by `ksql> show topics;` to show your connector success!)
```
ksql>
create stream stream_table (
    list_id int key,
    drama_name varchar(150),
    episodes int,
    orig_network varchar(75),
    score_list double,
    scored_by int,
    watchers double,
    imdb_desc varchar(255)) 
    WITH (kafka_topic='psql_connect01_kdrama_list', value_format='json', partitions=1
    );

-- or

create stream stream_table WITH (
    kafka_topic='psql_connect01_kdrama_list', value_format='avro', partitions=1
);
```
```
ksql>
CREATE TABLE final_table as
    SELECT 
        drama_name, 
        avg(score_list) as rating,
        sum(scored_by) as total_raters, 
        sum(watchers) as total_watchers  
    FROM stream_table st
    GROUP BY 
        drama_name
    emit changes;
```

## Insert More Data to kdrama_list Table on postgreSQL and check inside ksqlDB for updated query on stream_table
```
postgres=#
insert into kdrama_list values (11, 'Hospital Playlist', 12, '...', 8.5, 3, 7, '...');
insert into kdrama_list values (12, 'Hospital Playlist', 12, '...', 9.5, 1, 3, '...');
insert into kdrama_list values (13, 'Descendants of the Sun', 16, '...', 8.8, 6, 10, '...');
insert into kdrama_list values (14, 'Mouse', 20, '...', 9, 10, 10, '...');
insert into kdrama_list values (15, 'Vincenzo', 12, '...', 9.3, 13, 25, '...');
insert into kdrama_list values (16, 'Extraordinary Attorney Woo', 16, '...', 9.6, 4, 7, '...');
insert into kdrama_list values (17, 'Extraordinary Attorney Woo', 16, '...', 9.0, 8, 8, '...');
```

## Final Table Query
```
ksql>
select * from final_table WHERE rating > 9.1;
```