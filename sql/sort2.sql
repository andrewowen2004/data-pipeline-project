SELECT 
  strftime('%H', date) AS hour_of_day,
  COUNT(*) AS transaction_count,
  AVG(amount) AS avg_amount
FROM transactions
GROUP BY hour_of_day
ORDER BY hour_of_day;
