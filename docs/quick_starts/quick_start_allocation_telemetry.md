# Allocation Telemetry Quick Start <a name="top"/>

- [Allocation Telemetry Quick Start ](#allocation-telemetry-quick-start-)
  - [Explanation of Allocation Data](#explanation-of-allocation-data)
  - [Quick Start Scenario 1: Provide ALL Allocation Telemetry Data](#quick-start-scenario-1-provide-all-allocation-telemetry-data)
  - [Quick Start Scenario 2: Replicate Allocation Telemetry Data Over a Given Time Period](#quick-start-scenario-2-replicate-allocation-telemetry-data-over-a-given-time-period)
  - [Quick Start Scenario 3: Randomize Measurements in Allocation Telemetry Data](#quick-start-scenario-3-randomize-measurements-in-allocation-telemetry-data)
  - [Transmit Allocation Telemetry Records](#transmit-allocation-telemetry-records)

## Explanation of Allocation Data 
[Return to Top](#top)

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

If an `HOURLY` allocation is desired, CloudZero will:
* take the total spend of each product in a given hour (TOTAL PRODUCT SPEND)
* take the total usage by the customers in the hour (TOTAL CUSTOMER USAGE)
* determine each customer's percent of usage in the hour (CUSTOMER'S % OF USAGE)
* determine each customer's spend allocation with the following formula: CUSTOMER SPEND = CUSTOMER'S % OF USAGE * TOTAL PRODUCT SPEND

For example, in the hour `2024-02-08 00:00:00+00:00`, customer usage of `product A` totaled `100` units. `customer 3`'s usage is `30` units or `30%` of total usage. Therefore, `customer 3` receives 30% of `product A`'s cost in the hour. 

If a `DAILY` allocation is desired, CloudZero will:
* take the total spend of each product in a given day (TOTAL PRODUCT SPEND)
* take the total usage by the customers in the day (TOTAL CUSTOMER USAGE)
* determine each customer's percent of usage in the day (CUSTOMER'S % OF USAGE)
* determine each customer's spend allocation with the following formula: CUSTOMER SPEND = CUSTOMER'S % OF USAGE * TOTAL PRODUCT SPEND

For example, in the day `2024-02-08`, customer usage of `product A` totaled `100` units. `customer 3`'s usage is `30` units or `30%` of total usage. Therefore, `customer 3` receives 30% of `product A`'s cost in the day.

## Quick Start Scenario 1: Provide ALL Allocation Telemetry Data
[Return to Top](#top)

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

`allocation-config.json`
```json
{
    "version": "1",
    "template": {
      "timestamp": "$timestamp",
      "granularity": "HOURLY",
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

Generate Allocation Telemetry Records
```bash
uca -c allocation-config.json generate -o allocation-telemetry-records.json -i allocation-telemetry-data.csv
```

allocation-telemetry-records.json
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

## Quick Start Scenario 2: Replicate Allocation Telemetry Data Over a Given Time Period
[Return to Top](#top)

Daily Replication

If `granularity` in `allocation-config.json` is set to `DAILY`, the allocation telemetry data will be copied to each day in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then Feb. 9 and Feb. 10 will be given a copy of the data in `allocation-telemety-data.csv`

Hourly Replication

If `granularity` in `allocation-config.json` is set to `HOURLY`, the allocation telemetry data will be copied to each hour in a given time period.

For example, if the time period is `2024-02-09 - 2024-02-10`, then every hour in Feb. 9 and Feb. 10 will be given a copy of the data in `allocation-telemety-data.csv`

allocation-telemetry-data.csv

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

allocation-config.json
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

Generate Allocation Telemetry Records
```bash
uca -c allocation-config.json generate -o allocation-telemetry-records.json -i allocation-telemetry-data.csv -s 2024-02-09 -e 2024-02-10
```

allocation-telemetry-records.json
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

## Quick Start Scenario 3: Randomize Measurements in Allocation Telemetry Data
[Return to Top](#top)

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

`allocation-config.json`
```json
{
  "version": "1",
  "template": {
    "timestamp": "$timestamp",
    "granularity": "HOURLY",
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
    "api_key": "",
    "generate": {
      "mode": "jitter",
      "jitter": 10
    }
  }
}
```

`allocation-config.json` represent the config used by the CloudZero UCA Toolkit to generate the allocation telemetry records.

The values starting with `$` are placeholders that will be replaced by data in `allocation-telemetry-data.csv`.

If `mode` is jitter, defines the +/- random range to apply to the `$unit_value`

Generate Allocation Telemetry Records
```bash
uca -c allocation-config.json generate -o allocation-telemetry-records.json -i allocation-telemetry-data.csv
```

allocation-telemetry-records.json
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

## Transmit Allocation Telemetry Records
[Return to Top](#top)

Transmit Allocation Telemetry Records
```bash
uca -c allocation-config.json transmit -d file://allocation-telemetry-records.json
```