# Explanation of Allocation Data 
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


## HOURLY and DAILY Allocations

### HOURLY
If an `HOURLY` allocation is desired, CloudZero will:
* take the total spend of each product in a given hour (TOTAL PRODUCT SPEND)
* take the total usage by the customers in the hour (TOTAL CUSTOMER USAGE)
* determine each customer's percent of usage in the hour (CUSTOMER'S % OF USAGE)
* determine each customer's spend allocation with the following formula: CUSTOMER SPEND = CUSTOMER'S % OF USAGE * TOTAL PRODUCT SPEND

For example, in the hour `2024-02-08 00:00:00+00:00`, customer usage of `product A` totaled `100` units. `customer 3`'s usage is `30` units or `30%` of total usage. Therefore, `customer 3` receives 30% of `product A`'s cost in the hour. 

### DAILY
If a `DAILY` allocation is desired, CloudZero will:
* take the total spend of each product in a given day (TOTAL PRODUCT SPEND)
* take the total usage by the customers in the day (TOTAL CUSTOMER USAGE)
* determine each customer's percent of usage in the day (CUSTOMER'S % OF USAGE)
* determine each customer's spend allocation with the following formula: CUSTOMER SPEND = CUSTOMER'S % OF USAGE * TOTAL PRODUCT SPEND

For example, in the day `2024-02-08`, customer usage of `product A` totaled `100` units. `customer 3`'s usage is `30` units or `30%` of total usage. Therefore, `customer 3` receives 30% of `product A`'s cost in the day.

[Previous Page: Home](./quick_start_allocation_telemetry.md) | [Next Page: Quick Start Scenario 1](./scenario_1.md)