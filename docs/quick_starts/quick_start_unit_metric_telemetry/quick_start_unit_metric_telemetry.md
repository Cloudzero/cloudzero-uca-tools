# Unit Metric Telemetry Quick Start <a name="top"/>

1. [Explanation of Unit Metric Data](./explanation_of_unit_metric_data.md)

2. [Quick Start Scenario 1: User Provides ALL Unit Metric Telemetry Data](./scenario_1.md)

3. [Quick Start Scenario 2: UCA Toolkit Replicates Unit Metric Telemetry Data Over a Given Time Period](./scenario_2.md)

4. [Quick Start Scenario 3: UCA Toolkit Randomizes Metrics in Unit Metric Telemetry Data](./scenario_3.md)

5. [Transmit Unit Metric Telemetry Records](#transmit-unit-metric-telemetry-records)

## Transmit Unit Metric Telemetry Records

After you use the UCA Toolkit to generate Unit Metric Telemetry Records, you can use it to send them to the [CloudZero Telemetry API](https://docs.cloudzero.com/reference/telemetry-api-1)
```bash
uca -c unit-metric-config.json transmit -d file://unit-metric-telemetry-records.json
```

[Next Page: Explanation of Unit Metric Data](./explanation_of_unit_metric_data.md)