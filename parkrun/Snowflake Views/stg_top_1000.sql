create or replace view stg_top_1000 as 
with w_fastest as (
select  "parkrunID", "Name", "Gender", min(TOTALSEC) Fastest_time
from stg_parkrun_all_v 
group by "parkrunID", "Name", "Gender"
)
select  RANK() OVER (partition by NULL ORDER by  Fastest_time) As "Overall Rank" , 
        "Name", 
        "Gender",
        floor(Fastest_time/60) TimeMin,
        mod(Fastest_time,60)TimeSec, 
        floor(Fastest_time/60)||':'||LPAD(mod(Fastest_time,60),2,'0') "Time"
        
from w_fastest 
order by Fastest_time
LIMIT 1000
;