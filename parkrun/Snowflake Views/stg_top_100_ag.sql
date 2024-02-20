create or replace view stg_top_100_ag as 
with w_fastest as (
select  "parkrunID", "Name", "Gender", "AgeBracket", min(TOTALSEC) Fastest_time
from stg_parkrun_all_v 
where "AgeBracket" is not null
group by "parkrunID", "Name", "AgeBracket", "Gender"
)
select  RANK() OVER (partition by "AgeBracket" ORDER by  Fastest_time) "Age Bracket Rank" ,  
        "Name", 
        "Gender",
        "AgeBracket" as "AgeBracket",
        floor(Fastest_time/60) TimeMin,
        mod(Fastest_time,60)TimeSec, 
        floor(Fastest_time/60)||':'||LPAD(mod(Fastest_time,60),2,'0') "Time"
        
from w_fastest 
QUALIFY "Age Bracket Rank" <51
order by "AgeBracket", "Age Bracket Rank"
;