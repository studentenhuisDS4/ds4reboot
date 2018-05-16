SELECT turf_count, turf_time, turf_to, turf_type 
FROM bierlijst_turf
WHERE turf_to = 'kalle'
AND turf_time > '2016-12-16'
ORDER BY turf_time DESC;
