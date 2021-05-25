# CloudZero UCA Tools
Utilities for generating, transforming and transmitting UCA data

## Features
* Generate UCA v1.2 data
* Transmit UCA v1.2 data to CloudZero (using the CloudZero UCA API)
* Transform ELB/ALB and CloudFront logs into UCA data (Coming Soon!)

## Installation
      $ pip install --user cloudzero-uca-tools

## Usage
CloudZero UCA tools exist to produce UCA events that can then be transmitted to the CloudZero API
for analysis and processing. To use the CloudZero API, you should first obtain an API key from https://app.cloudzero.com/organization/api-keys

### Data Generation
UCA data generation is useful when you need to account for static assets and cost allocations
that need to be accounted for to fill gaps in your UCA data or for testing purposes.
####Examples

#####Help:
    $ uca generate --help
    Usage: uca generate [OPTIONS]
    
    Options:
      -s, --start TEXT          start datetime <YYYY-MM-DD HH:MM:SS>
      -e, --end TEXT            End datetime <YYYY-MM-DD HH:MM:SS>
      --today                   Generate events for the current day
      -c, --configuration TEXT  UCA configuration file (JSON)  [required]
      -d, --data TEXT           Input UCA data (CSV)  [required]
      -o, --output TEXT         Instead of sending events to the API, append the
                                events to an output file
      -k, --api-key TEXT        API Key to use
      -dry, --dry-run           Perform a dry run, read and transform the data but
                                do not send it to the API
      --help                    Show this message and exit.

##### Generate
Generate UCA data between 2021-03-13 and 2021-04-07 using data/configuration.json and data/data.csv as input. Perform only a dry run and do not send the results to the CloudZero API

    $ uca generate -s 2021-03-13 -e 2021-04-07 -c data/configuration.json -d data/data.csv --dry-run

#### Configuration File
The generate configuration file is a JSON formatted definition of the UCA template
you wish to use and the settings that should be applied when injecting data. You 
can learn more [here about the UCA format and our UCA Telemetry API](https://docs.cloudzero.com/reference#telemetry).

    {
      "template": {
        "timestamp": "$timestamp",                  # Timestamp will be replaced automatically
        "granularity": "DAILY",                     # Granularity can be HOURLY or DAILY
        "cost-context": "Cost-Per-Fake-Customer",   # You can have up to 5 telemetry streams per context
        "id": "$unit_id",                           # Will be replaced using data from your data CSV
        "target": {},                               # Use {} to map to all spend or use a combination of tags and keywords to get more specific
        "telemetry-stream": "test-data",            # Unique name for this telemetry stream          
        "value": "$unit_value"                      # Will be replaced using generated data or data from your data CSV
      },
      "settings": {
        "version": "v1.2",                          # Currently only v1.2 is supported
        "mode": "exact",                            # Can be exact, random, jitter or allocation
        "jitter": 15,                               # if mode is jitter, this value defines the range
        "allocation": 100000                        # if mode is allocation, this value defines the total amount to be allocated
        "api_key": "<YOUR API KEY HERE>"            # Also can be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys
      }
    }

#### Data CSV
The data CSV defines the input data you wish to feed into the template. This tool will produce
matching UCA records for all rows in your data CSV for each hour or day as defined. The following
example has 13 "customers" and can be used as input for all configuration modes.

        unit_id,unit_value,unit_allocation
        Sunbank,37,8.5574
        SoftwareCorp,17,0.4091
        "Parts, Inc.",140,10.9955
        Transport Co.,25,6.3033
        "WeShipit, Inc.",124,23.7549
        CapitalTwo,90,1.5231
        Bank of Sokovia,43,0.1198
        Makers,9,1.0767
        StateEx,40,3.5057
        Flitter,15,22.9554
        Pets2you,78,6.3358
        Hooli,23,4.3294
        Massive Dynamic,42,10.1339

#### Example output
Together this configuration and data will produce UCA events similar to the following:

    {'timestamp': '2021-03-22 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'StateEx', 'target': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'Hooli', 'target': {}, 'telemetry-stream': 'test-data', 'value': '23.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'Sunbank', 'target': {}, 'telemetry-stream': 'test-data', 'value': '37.0000'}
    {'timestamp': '2021-04-06 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'Transport Co.', 'target': {}, 'telemetry-stream': 'test-data', 'value': '25.0000'}
    {'timestamp': '2021-03-19 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'StateEx', 'target': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}