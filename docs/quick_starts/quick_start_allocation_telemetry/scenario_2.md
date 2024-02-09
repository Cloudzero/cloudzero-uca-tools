# Quick Start Scenario 2: UCA Toolkit Replicates Allocation Telemetry Data Over a Given Time Period
[Return Home](./quick_start_allocation_telemetry.md#allocation-telemetry-quick-start)

## Daily Replication

If `granularity` in `allocation-config.json` is set to `DAILY`, the allocation telemetry data will be copied to each day in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then Feb. 9 and Feb. 10 will be given a copy of the data in `allocation-telemety-data.csv`

## Hourly Replication

If `granularity` in `allocation-config.json` is set to `HOURLY`, the allocation telemetry data will be copied to each hour in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then every hour in Feb. 9 and Feb. 10 will be given a copy of the data in `allocation-telemety-data.csv`

## Allocation Telemetry Data

`allocation-telemetry-data.csv`

| unit_value | filter_dimension | filter_dimension_group | element_id |
|------------|------------------|------------------------|------------|
| 10         | product          | product A              | customer 1 |
| 10         | product          | product A              | customer 2 |
| 20         | product          | product A              | customer 3 |
| 30         | product          | product A              | customer 4 |
| 30         | product          | product A              | customer 5 |
| 10         | product          | product B              | customer 1 |
| 10         | product          | product B              | customer 2 |
| 20         | product          | product B              | customer 3 |
| 30         | product          | product B              | customer 4 |
| 30         | product          | product B              | customer 5 |

`allocation-telemetry-data.csv` represents measurements of customer usage for two products:
  * unit_value: the amount of usage
  * filter_dimension: category of cloud infrastructure used
  * filter_dimension_group: cloud infrastructure used
  * element_id: ID of customer

## Allocation Telemetry Config

`allocation-config.json`
```json
{
    "version": "1",
    "template": {
      "timestamp": "$timestamp",
      "granularity": "DAILY",
      "element-name": "$element_id",
      "filter": {
        "custom:$filter_dimension": [
          "$filter_dimension_group"
        ]
      },
      "telemetry-stream": "product-cost-per-customer-v1",
      "value": "$unit_value"
    },
    "settings": {
      "api_key": "<CLOUDZERO API KEY>",
      "generate": {"mode": "exact"}
    }
  }
```
`allocation-config.json` represent the config used by the CloudZero UCA Toolkit to generate the allocation telemetry records.

The values starting with `$` are placeholders that will be replaced by data in `allocation-telemetry-data.csv`.

## Generate Allocation Telemetry Records
```bash
uca -c allocation-config.json generate -o allocation-telemetry-records.json -i allocation-telemetry-data.csv -s 2024-02-09 -e 2024-02-10
```

[Transmit Allocation Telemetry Records](./quick_start_allocation_telemetry.md#transmit-allocation-telemetry-records)

`allocation-telemetry-records.json`
```json
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 1", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 2", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 3", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 4", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 5", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 1", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 2", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 3", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 4", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-09 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 5", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 1", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 2", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 3", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 4", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 5", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 1", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 2", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 3", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 4", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-10 00:00:00+00:00", "granularity": "DAILY", "element-name": "customer 5", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
```

[Previous Page: Quick Start Scenario 1](./scenario_1.md#quick-start-scenario-1-user-provides-all-allocation-telemetry-data) | [Next Page: Quick Start Scenario 3](./scenario_3.md#quick-start-scenario-3-uca-toolkit-randomizes-measurements-in-allocation-telemetry-data)