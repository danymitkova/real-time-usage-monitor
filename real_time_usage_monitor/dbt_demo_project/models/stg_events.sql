-- staging model placeholder
select * from {{ source('delta', 'usage_agg') }}