# Quick Start Scenario 1: User Provides ALL Allocation Telemetry Data
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
      "api_key": "<CLOUDZERO API KEY>",
      "generate": {"mode": "exact"}
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
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 1", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 2", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 3", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 4", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-08 00:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 5", "filter": {"custom:product": ["product A"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 1", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 2", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "10.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 3", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "20.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 4", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
{"timestamp": "2024-02-08 01:00:00+00:00", "granularity": "HOURLY", "element-name": "customer 5", "filter": {"custom:product": ["product B"]}, "telemetry-stream": "product-cost-per-customer-v1", "value": "30.00"}
```

[Previous Page: Explanation of Allocation Data](./explanation_of_allocation_data.md) | [Next Page: Quick Start Scenario 2](./scenario_2.md)