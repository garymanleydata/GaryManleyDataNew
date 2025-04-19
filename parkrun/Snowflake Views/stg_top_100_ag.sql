create or replace view stg_top_100_ag as 
with w_fastest as (
/*This view is ranking the fastest times for each AgeBracket partition in the stg_parkrun_all_v table. It is:

Using a CTE (Common Table Expression) named w_fastest to select the parkrunID, Name, Gender, AgeBracket and fastest time (min of TOTALSEC) for each unique combination, grouping by those columns.
Then in the outer query, it is ranking those fastest times for each AgeBracket partition using the RANK() function.
It is also selecting the Name, Gender, AgeBracket, and formatting the fastest time as minutes, seconds and a combined time string.
This view will contain the top 100 fastest times per AgeBracket. */
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