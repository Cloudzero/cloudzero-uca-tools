# Quick Start Scenario 3: UCA Toolkit Randomizes Metrics in Allocation Telemetry Data
[Return Home](./quick_start_unit_metric_telemetry.md#unit-metric-telemetry-quick-start)

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

If `mode` is jitter, defines the +/- random range to apply to the `$unit_value`

For example, if `jitter` is set to `1000`, then a random number between `1` and `1000` will be added or substracted from each value in the `unit_value` column.

Each value will have its own random `jitter`.

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
    "generate": {
      "mode": "jitter",
      "jitter": 1000
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
{"timestamp": "2024-02-08 00:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "10151.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "9165.00"}
{"timestamp": "2024-02-08 02:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "20789.00"}
{"timestamp": "2024-02-08 03:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "29937.00"}
{"timestamp": "2024-02-08 04:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "30221.00"}
{"timestamp": "2024-02-08 05:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "10132.00"}
{"timestamp": "2024-02-08 06:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "9624.00"}
{"timestamp": "2024-02-08 07:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "20063.00"}
{"timestamp": "2024-02-08 08:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "30876.00"}
{"timestamp": "2024-02-08 09:00:00+00:00", "associated_cost": {"custom:product": "product A"}, "metric-name": "hourly-cost-per-ad-impression-v1", "value": "29353.00"}

```

[Previous Page: Quick Start Scenario 2](./scenario_2.md) | [Next Page: Home](./quick_start_unit_metric_telemetry.md)