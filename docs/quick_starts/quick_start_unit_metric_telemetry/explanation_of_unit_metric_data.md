# Explanation of Unit Metric Data
[Return Home](./quick_start_unit_metric_telemetry.md)

## Unit Metric Telemetry Data

`unit-metric-telemetry-data.csv`

| timestamp                 | unit_value | filter_dimension_1 | filter_dimension_1_group |
| ------------------------- | ---------- | ------------------ | ------------------------ |
| 2024-02-08 00:00:00+00:00 | 10000      | product            | product A                |
| 2024-02-08 01:00:00+00:00 | 10000      | product            | product A                |
| 2024-02-08 02:00:00+00:00 | 20000      | product            | product A                |
| 2024-02-08 03:00:00+00:00 | 30000      | product            | product A                |
| 2024-02-08 04:00:00+00:00 | 30000      | product            | product A                |
| 2024-02-08 05:00:00+00:00 | 10000      | product            | product A                |
| 2024-02-08 06:00:00+00:00 | 10000      | product            | product A                |
| 2024-02-08 07:00:00+00:00 | 20000      | product            | product A                |
| 2024-02-08 08:00:00+00:00 | 30000      | product            | product A                |
| 2024-02-08 09:00:00+00:00 | 30000      | product            | product A                |

`unit-metric-telemetry-data.csv` represents unit counts processed by a product. In this scenario, the unit is ad impression:
  * `timestamp`: when the ad impressions were processed
  * `unit_value`: the number of ad impressions processed
  * `filter_dimension_1`: catagory of cloud infrastructure used to process ad impressions
  * `filter_dimension_1_filter_group`: cloud infrastructure used to process ad impressions

[Previous Page: Home](./quick_start_unit_metric_telemetry.md) | [Next Page: Quick Start Scenario 1](./scenario_1.md)