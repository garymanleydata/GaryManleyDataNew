-- Snowflake checks 

GRANT SELECT on workspace_64748299 to KEBOOLA_7127_RO;

--2017-11-18 1 diff
with w_agg as (
SELECT to_date("Date",'DD/MM/YYYY') event_date, count(*) Total
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
group by to_date("Date",'DD/MM/YYYY')
), 
w_eh as (select "DATE" , dateadd(year, 2000, "DATE") event_date , total, "EVENTNUM"
FROM KEBOOLA_7127.WORKSPACE_64748299."EVENT_HISTORY")
select w_agg.event_date, w_agg.total, w_eh.total, "EVENTNUM"
from w_agg
left outer join w_eh on w_agg . event_date = w_eh.event_date
order by w_agg.event_date;

select "DATE" , dateadd(year, 2000, "DATE") , total
FROM KEBOOLA_7127.WORKSPACE_64748299."EVENT_HISTORY"
;

-- 332
insert into KEBOOLA_7127.WORKSPACE_64748299."parkrunAll" ("Date","Position","Name")
SELECT pa."Date", 321 as "Position", "Name" 
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll" pa
where to_date("Date",'DD/MM/YYYY') = '2023-05-06' 
and "Position" = 91
;


SELECT "parkrunID", count(*) Total
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
group by "parkrunID"
order by 2 desc;


SELECT *--"Date", COUNT(*)
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
WHERE upper("parkrunID") is NULL 
and "Gender" is not null
;


SELECT "Date", COUNT(*)
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
WHERE "AgeBracket" is NULL
GROUP BY "Date"
;



UPDATE KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
SET "parkrunID" = 4153607 
WHERE "Name" = 'Garfield KENNEDY'
AND upper("parkrunID") is NULL 
and "Gender" is not null
;

SELECT *
FROM KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
WHERE "Name" = 'David CRAVEN'
;

select * from  KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
order by "TimeMin" , "TimeSec"
 ; 

UPDATE  KEBOOLA_7127.WORKSPACE_64748299."parkrunAll"
SET "TimeMin" = 61
where "TimeMin" = 1
 ; 


 select * 
 from KEBOOLA_7127.WORKSPACE_64748299."EVENT_HISTORY"; 

 INSERT INTO KEBOOLA_7127.WORKSPACE_64748299."EVENT_HISTORY"
 SELECT 571 EVENTNUM, 
        '0024-02-17' "DATE",
        299 TOTAL, 
        25 VOLUNTEERS,
        'Stuart PELLING' MALE_NAME, 
        '17:17' MALE_TIME,
        'Aislinn DARVELL' FEMALE_NAME,	
        '19:44' FEMALE_TIME
        