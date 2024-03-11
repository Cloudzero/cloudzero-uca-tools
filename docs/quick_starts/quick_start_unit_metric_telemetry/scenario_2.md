# Quick Start Scenario 2: UCA Toolkit Replicate Unit Metric Telemetry Data Over a Given Time Period
[Return Home](./quick_start_unit_metric_telemetry.md)

## Daily Replication

If `granularity` in `unit-metric-config.json` is set to `DAILY`, the unit metric telemetry data will be copied to each day in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then Feb. 9 and Feb. 10 will be given a copy of the data in `unit-metric-telemety-data.csv`

## Hourly Replication

If `granularity` in `unit-metric-config.json` is set to `HOURLY`, the unit metric telemetry data will be copied to each hour in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then every hour in Feb. 9 and Feb. 10 will be given a copy of the data in `unit-metric-telemety-data.csv`

## Unit Metric Telemetry Data

`unit-metric-telemetry-data.csv`

| unit_value | filter_dimension_1 | filter_dimension_1_group |
|------------|--------------------|--------------------------|
| 10000      | product            | product A                |
| 10000      | product            | product A                |
| 20000      | product            | product A                |
| 30000      | product            | product A                |
| 30000      | product            | product A                |
| 10000      | product            | product A                |
| 10000      | product            | product A                |
| 20000      | product            | product A                |
| 30000      | product            | product A                |
| 30000      | product            | product A                |

`unit-metric-telemetry-data.csv` represents unit counts processed by a product. In this scenario, the unit is ad impressions:
  * `unit_value`: the number of ad impressions processed
  * `filter_dimension_1`: catagory of cloud infrastructure used to process ad impressions
  * `filter_dimension_1_filter_group`: cloud infrastructure used to process ad impressions

## Unit Metric Telemetry Config

`unit-metric-config.json`
```json
{
  "version": "1",
  "template": {
    "metric-name": "cost-per-hourly-ad-impressions-v1",
    "associated_cost": {
      "custom:$filter_dimension_1": "$filter_dimension_1_group"
    },
    "timestamp": "$timestamp",
    "value": "$unit_value"
  },
  "settings": {
    "api_key": "<CLOUDZERO API KEY>",
    "transmit_type": "sum",
    "generate": {
      "mode": "exact"
    }
  }
}
```
`unit-metric-config.json` represent the config used by the CloudZero UCA Toolkit to generate the unit metric telemetry records.

The values starting with `$` are placeholders that will be replaced by data in `unit-metric-telemetry-data.csv`.

## Generate Unit Metric Telemetry Records
```bash
uca -c unit-metric-config.json generate -o unit-metric-telemetry-records.json -i unit-metric-telemetry-data.csv -s 2024-02-09 -e 2024-02-10
```
[Transmit Unit Metric Telemetry Records](./quick_start_unit_metric_telemetry.md#transmit-unit-metric-telemetry-records)

`unit-metric-telemetry-records.json`
```json
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "cost-per-daily-ad-impressions-v1", "value": "30000.00"}
```

[Previous Page: Quick Start Scenario 1](./scenario_1.md) | [Next Page: Quick Start Scenario 3](./scenario_3.md)