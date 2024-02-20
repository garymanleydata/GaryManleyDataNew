create or replace view stg_latest_event_all_v as 
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
        s."Position",
        s."Name",
        s."Gender", 
        s."AgeBracket",
        s."Club", 
        s."DISPLAYTIME" as "Time",
        (CASE WHEN pb."parkrunID" IS NULL THEN NULL ELSE 'PB' END) AS "PB" , 
        s."TOTALSEC" as TimeSeconds
from stg_parkrun_all_v s
LEFT OUTER JOIN w_pb_list pb on s."EVENTNUM" = pb."EVENTNUM" 
                            and s."parkrunID" = pb."parkrunID"
WHERE s."EVENTNUM" = (select max(s2."EVENTNUM") FROM stg_parkrun_all_v s2)
ORDER BY "Position"
        ;