SELECT Subject, COUNT(*) AS count
FROM transactions
WHERE Subject IS NOT NULL AND Subject != ''
GROUP BY Subject
ORDER BY count DESC;


