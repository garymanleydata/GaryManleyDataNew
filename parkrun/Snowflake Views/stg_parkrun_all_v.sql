create or replace view stg_parkrun_all_v 
COMMENT = 'Joining the parkrun base views together and calc total time'
as
with w_agg as (
SELECT to_date("Date",'DD/MM/YYYY') event_date, p.*
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll" p
), 
w_eh as (select "DATE" , dateadd(year, 2000, "DATE") event_date , total, "EVENTNUM"
FROM KEBOOLA_7127.WORKSPACE_64748299."EVENT_HISTORY")
select  a."EVENT_DATE" as EventDate, 
        e."EVENTNUM" as EventNum, 
        e."TOTAL" as TotalAthletes, 
        a."Position", 
        a."parkrunID", 
        a."Name", 
        a."Gender", 
        a."AgeBracket", 
        a."Club", 
        a."TimeMin", 
        a."TimeSec", 
        (a."TimeMin"*60 ) + a."TimeSec" TotalSec,
        a."TimeMin" ||':'||LPAD(a."TimeSec",2,'0') DisplayTime, 
        width_bucket(a."TimeMin",15,110,20) Mins_5_bucket
from w_agg a
left outer join w_eh e on a.event_date = e.event_date; 