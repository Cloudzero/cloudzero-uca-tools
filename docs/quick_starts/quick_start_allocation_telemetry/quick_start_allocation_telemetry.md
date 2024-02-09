# Allocation Telemetry Quick Start <a name="top"/>

1. [Explanation of Allocation Data](./explanation_of_allocation_data.md#explanation-of-allocation-data)

2. [Quick Start Scenario 1: User Provides ALL Allocation Telemetry Data](./scenario_1.md#quick-start-scenario-1-user-provides-all-allocation-telemetry-data)

3. [Quick Start Scenario 2: UCA Toolkit Replicates Allocation Telemetry Data Over a Given Time Period](./scenario_2.md#quick-start-scenario-2-uca-toolkit-replicates-allocation-telemetry-data-over-a-given-time-period)

4. [Quick Start Scenario 3: UCA Toolkit Randomizes Measurements in Allocation Telemetry Data](./scenario_3.md#quick-start-scenario-3-uca-toolkit-randomizes-measurements-in-allocation-telemetry-data)

5. [Transmit Allocation Telemetry Records](#transmit-allocation-telemetry-records)

## Transmit Allocation Telemetry Records
[Return to Top](#top)

Transmit Allocation Telemetry Records
```bash
uca -c allocation-config.json transmit -d file://allocation-telemetry-records.json
```