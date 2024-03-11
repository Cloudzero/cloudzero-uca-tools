# Quick Start Scenario 3: UCA Toolkit Randomizes Measurements in Allocation Telemetry Data
[Return Home](./quick_start_allocation_telemetry.md)

## Allocation Telemetry Data

`allocation-telemetry-data.csv`

| timestamp                 | unit_value | filter_dimension | filter_dimension_group | element_id |
|---------------------------|------------|------------------|------------------------|------------|
| 2024-02-08 00:00:00+00:00 | 10         | product          | product A              | customer 1 |
| 2024-02-08 00:00:00+00:00 | 10         | product          | product A              | customer 2 |
| 2024-02-08 00:00:00+00:00 | 20         | product          | product A              | customer 3 |
| 2024-02-08 00:00:00+00:00 | 30         | product          | product A              | customer 4 |
| 2024-02-08 00:00:00+00:00 | 30         | product          | product A              | customer 5 |
| 2024-02-08 01:00:00+00:00 | 10         | product          | product B              | customer 1 |
| 2024-02-08 01:00:00+00:00 | 10         | product          | product B              | customer 2 |
| 2024-02-08 01:00:00+00:00 | 20         | product          | product B              | customer 3 |
| 2024-02-08 01:00:00+00:00 | 30         | product          | product B              | customer 4 |
| 2024-02-08 01:00:00+00:00 | 30         | product          | product B              | customer 5 |

`allocation-telemetry-data.csv` represents measurements of customer usage for two products:
  * `timestamp`: when the customer used the product
  * `unit_value`: the amount of usage
  * `filter_dimension`: category of cloud infrastructure used
  * `filter_dimension_group`: cloud infrastructure used
  * `element_id`: ID of customer

## Allocation Telemetry Config

If `mode` is jitter, defines the +/- random range to apply to the `$unit_value`

For example, if `jitter` is set to `10`, then a random number between `1` and `10` will be added or substracted from each value in the `unit_value` column.

Each value will have its own random `jitter`.

`allocation-config.json`
```json
{
  "version": "1",
  "template": {
    "telemetry-stream": "product-cost-per-customer-v1",
    "granularity": "HOURLY",
    "filter": {
      "custom:$filter_dimension": [
        "$filter_dimension_group"
      ]
    },
    "timestamp": "$timestamp",
    "element-name": "$element_id",
    "value": "$unit_value"
  },
  "settings": {
    "api_key": "",
    "transmit_type": "sum",
    "generate": {
      "mode": "jitter",
      "jitter": 10
    }
  }
}
```

`allocation-config.json` represent the config used by the CloudZero UCA Toolkit to generate the allocation telemetry records.

The values starting with `$` are placeholders that will be replaced by data in `allocation-telemetry-data.csv`.

## Generate Allocation Telemetry Records
```bash
uca -c allocation-config.json generate -o allocation-telemetry-records.json -i allocation-telemetry-data.csv
```

[Transmit Allocation Telemetry Records](./quick_start_allocation_telemetry.md#transmit-allocation-telemetry-records)

`allocation-telemetry-records.json`
```json
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 1", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "5.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 2", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "18.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 3", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "14.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 4", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "36.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 5", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "34.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 1", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "13.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 2", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "12.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 3", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "29.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 4", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 5", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "40.00"}
```

[Previous Page: Quick Start Scenario 2](./scenario_2.md) | [Next Page: Home](./quick_start_allocation_telemetry.md)