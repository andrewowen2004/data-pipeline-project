WITH stats AS (
  SELECT
    AVG(amount) AS mean,
    AVG(amount * amount) - AVG(amount) * AVG(amount) AS variance
  FROM transactions
),
outliers AS (
  SELECT
    t.*,
    s.mean,
    s.variance,
    ABS(t.amount - s.mean) AS deviation
  FROM
    transactions t,
    stats s
)
SELECT *
FROM outliers
WHERE deviation > 3 * sqrt(variance);
