create or replace view stg_top1 as 
with w_ff as (
select "parkrunID", "Name", min("EVENTNUM") first_first, count(*) total_p1
from stg_parkrun_all_v
where "Position" = 1
and "parkrunID" is not null
--and "parkrunID" = 500760
GROUP BY "parkrunID","Name")
select f."Name", sum(case when a."parkrunID" is null then 0 else 1 end) "Events Pre First P1", total_p1 "Total 1st Places"
from w_ff f
left outer join stg_parkrun_all_v a on a."parkrunID" = f."parkrunID" and a."EVENTNUM" < f.first_first
group by a."parkrunID", f."Name", total_p1
order by total_p1 desc;
