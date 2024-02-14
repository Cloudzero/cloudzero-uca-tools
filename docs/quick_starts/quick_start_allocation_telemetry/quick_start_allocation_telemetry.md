# Allocation Telemetry Quick Start <a name="top"/>

1. [Explanation of Allocation Data](./explanation_of_allocation_data.md)

2. [Quick Start Scenario 1: User Provides ALL Allocation Telemetry Data](./scenario_1.md)

3. [Quick Start Scenario 2: UCA Toolkit Replicates Allocation Telemetry Data Over a Given Time Period](./scenario_2.md)

4. [Quick Start Scenario 3: UCA Toolkit Randomizes Measurements in Allocation Telemetry Data](./scenario_3.md)

5. [Transmit Allocation Telemetry Records](#transmit-allocation-telemetry-records)

## Transmit Allocation Telemetry Records

After you use the UCA Toolkit to generate Allocation Telemetry Records, you can use it to send them to the [CloudZero Telemetry API](https://docs.cloudzero.com/reference/telemetry-api-1)
```bash
uca -c allocation-config.json transmit -d file://allocation-telemetry-records.json
```

[Next Page: Explanation of Allocation Data](./explanation_of_allocation_data.md)