create or replace view stg_club_list_v as 
select  "Club", 
        count(*) "Total Runs", 
        count(distinct "parkrunID") "Total Runners"
from stg_parkrun_all_v a
where "Club" is not null
group by  "Club"
order by 2 desc
limit 20; 