SELECT
  id,
  DATETIME(time, 'unixepoch', 'localtime') as t,
  time,
  activity,
  details
FROM activity_log
