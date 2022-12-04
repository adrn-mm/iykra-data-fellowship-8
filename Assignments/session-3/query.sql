SELECT
  geoNetwork.country,
  date,
  channelGrouping,
  totals.transactions
FROM
  `bigquery-public-data.google_analytics_sample.ga_sessions_20170801`
WHERE
  totals.transactions IS NOT NULL