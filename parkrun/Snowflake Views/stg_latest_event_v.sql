create or replace view stg_latest_event_v as 
with w_pb_calc as (
select a."EVENTNUM", 
       a."parkrunID", 
       a."TOTALSEC", 
       min(b."TOTALSEC") MIN_PREV_TIME
from stg_parkrun_all_v a
inner join stg_parkrun_all_v b on a."parkrunID" = b."parkrunID"
                                and b."EVENTNUM" < a."EVENTNUM"
group by a."EVENTNUM", 
       a."parkrunID", 
       a."TOTALSEC"
        ), 
w_pb_list as (
select EVENTNUM, "parkrunID"
from w_pb_calc
WHERE TOTALSEC < MIN_PREV_TIME
)
select  "EVENTDATE" "Event Date", 
        s."EVENTNUM" "Event Number", 
        COUNT(*) "Total Athletes", 
        SUM(CASE WHEN UPPER("Gender") = 'MALE' THEN 1 ELSE 0 END) AS "Male Count",
        SUM(CASE WHEN UPPER("Gender") = 'FEMALE' THEN 1 ELSE 0 END) AS "Female Count", 
        SUM(CASE WHEN "MINS_5_BUCKET" = 1 THEN 1 ELSE 0 END) AS "Sub 20 Count" , 
        SUM(CASE WHEN "MINS_5_BUCKET" = 2 THEN 1 ELSE 0 END) AS "20-24:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 3 THEN 1 ELSE 0 END) AS "25-29:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 4 THEN 1 ELSE 0 END) AS "30-34:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 5 THEN 1 ELSE 0 END) AS "35-40:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 6 THEN 1 ELSE 0 END) AS "40-44:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 7 THEN 1 ELSE 0 END) AS "45-49:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 8 THEN 1 ELSE 0 END) AS "50-54:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 9 THEN 1 ELSE 0 END) AS "55-59:59 Count",
        SUM(CASE WHEN "MINS_5_BUCKET" = 9 THEN 1 ELSE 0 END) AS "60+ Count" , 
        SUM(CASE WHEN pb."parkrunID" IS NULL THEN 0 ELSE 1 END) AS "PB Count" 
from stg_parkrun_all_v s
LEFT OUTER JOIN w_pb_list pb on s."EVENTNUM" = pb."EVENTNUM" 
                            and s."parkrunID" = pb."parkrunID"
WHERE s."EVENTNUM" = (select max(s2."EVENTNUM") FROM stg_parkrun_all_v s2)
GROUP BY "EVENTDATE" , 
        s."EVENTNUM"
        ;
