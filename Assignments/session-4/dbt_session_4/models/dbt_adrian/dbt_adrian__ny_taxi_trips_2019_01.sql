with source_ny_trips_2019_01 as (
    select * from {{ source('dbt-adrian', 'ny_taxi_trips_2019_01') }}
),

final as (
    select * from source_ny_trips_2019_01
)

select * from final