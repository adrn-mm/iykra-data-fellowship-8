-- # 1. Connector Creation - https://debezium.io/documentation/reference/stable/connectors/postgresql.html#postgresql-connector-properties
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

-- # 4. Stream Creation
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

-- # 5. Table Creation
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

-- 7. Final Table
select * from final_table WHERE rating > 9.1;