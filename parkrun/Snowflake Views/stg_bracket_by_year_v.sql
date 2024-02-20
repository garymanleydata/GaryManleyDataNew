create or replace view stg_bracket_by_year_v as
select  extract(year from "Event Date") "Event Year", 
        SUM("Sub 20 Count") / SUM("Total Athletes") *100 "Percent Sub 20",
        SUM("20-24:59 Count") / SUM("Total Athletes") *100 "Percent 20-24:59 Count",
        SUM("25-29:59 Count") / SUM("Total Athletes") *100 "Percent 25-29:59 Count",
        SUM("30-34:59 Count") / SUM("Total Athletes") *100 "Percent 30-34:59 Count",
        SUM("35-40:59 Count") / SUM("Total Athletes") *100 "Percent 35-40:59 Count",
        SUM("40-44:59 Count") / SUM("Total Athletes") *100 "Percent 40-44:59 Count",
        SUM("45-49:59 Count") / SUM("Total Athletes") *100 "Percent 45-49:59 Count",
        SUM("50-54:59 Count") / SUM("Total Athletes") *100 "Percent 50-54:59 Count",
        SUM("55-59:59 Count") / SUM("Total Athletes") *100 "Percent 55-59:59 Count",
        SUM("60+ Count") / SUM("Total Athletes") *100 "Percent 60+ Count"
from stg_event_summy_v
GROUP BY extract(year from "Event Date")
ORDER BY 1
;