# Quick Start Scenario 1: User Provides ALL Unit Metric Telemetry Data
[Return Home](./quick_start_unit_metric_telemetry.md)

## Unit Metric Telemetry Data

`unit-metric-telemetry-data.csv`

| timestamp                 | unit_value | filter_dimension_1 | filter_dimension_1_group |
|---------------------------|------------|--------------------|--------------------------|
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

`unit-metric-telemetry-data.csv` represents unit counts processed by a product. In this scenario, the unit is ad impressions:
    * `timestamp`: when the ad impressions were processed
    * `unit_value`: the number of ad impressions processed
    * `filter_dimension_1`: catagory of cloud infrastructure used to process ad impressions
    * `filter_dimension_1_filter_group`: cloud infrastructure used to process ad impressions

## Unit Metric Telemetry Config

`unit-metric-config.json`
```json
{
  "version": "1",
  "template": {
    "timestamp": "$timestamp",
    "granularity": "HOURLY",
    "associated-cost": {
      "custom:$filter_dimension_1": "$filter_dimension_1_group"
    },
    "metric-name": "cost-per-hourly-ad-impressions-v1",
    "value": "$unit_value"
  },
  "settings": {
    "api_key": "<CLOUDZERO API KEY>",
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
uca -c unit-metric-config.json generate -o unit-metric-telemetry-records.json -i unit-metric-telemetry-data.csv
```
[Transmit Unit Metric Telemetry Records](./quick_start_unit_metric_telemetry.md#transmit-unit-metric-telemetry-records)

`unit-metric-telemetry-records.json`
```json
{"timestamp": "2024-02-08 00:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-08 02:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-08 03:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-08 04:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-08 05:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-08 06:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "10000.00"}
{"timestamp": "2024-02-08 07:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "20000.00"}
{"timestamp": "2024-02-08 08:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "30000.00"}
{"timestamp": "2024-02-08 09:00:00+00:00", "associated-cost": {"custom:product": "product A"}, "metric-name": "cost-per-hourly-ad-impressions-v1", "value": "30000.00"}
```

[Previous Page: Explanation of Unit Metric Data](./explanation_of_unit_metric_data.md) | [Next Page: Quick Start Scenario 2](./scenario_2.md)