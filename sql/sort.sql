SELECT subject, COUNT(*) AS transaction_count
FROM transactions
GROUP BY subject
ORDER BY transaction_count DESC;
