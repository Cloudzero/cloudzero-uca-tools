# CloudZero UCA Toolkit
Utilities for generating, transforming and transmitting unit cost analytics (UCA) data to the CloudZero API.
Visit our [UCA documentation](https://docs.cloudzero.com/docs/enhanced-unit-cost-analytics) to learn more about
[CloudZero](https://www.cloudzero.com) and our enhanced unit cost analytics capabilities.

## Features
* Transmit UCA data to CloudZero (using the CloudZero UCA API)
* Generate UCA data

## prerequisites
* Tested on MacOS, should probably run on Linux in general
* Python 3.8 or newer
* `pip` or your favorite method of installing packages from PyPi. Have you considered [pipx](https://pypa.github.io/pipx/)?

## Installation
      $ pipx install cloudzero-uca-tools

## General Usage
CloudZero UCA tools exist to produce UCA events that can then be transmitted to the CloudZero API
for analysis and processing. To use the CloudZero API, you should first obtain an [API key](https://app.cloudzero.com/organization/api-keys)
from https://app.cloudzero.com/organization/api-keys

    $ uca
    Usage: uca [OPTIONS] COMMAND [ARGS]...
    
      CloudZero Unit Cost Analytics Toolkit
    
    Options:
      --version                 Show the version and exit.
      -c, --configuration TEXT  UCA configuration file (JSON)
      -o, --output TEXT         Instead of sending events to the API, write
                                events to an output file (note: will overwrite file if it exists)
      -dry, --dry-run           Perform a dry run, read and transform the data but
                                do not send it to the API. Sample events will be output to the screen
      -k, --api-key TEXT        API Key to use
      --help                    Show this message and exit.
    
    Commands:
      transmit
      generate

### Basic Configuration
The following is a minimal configuration file for transmitting data to the CloudZero API 
(if you don't want to specify the API on the command line, otherwise no configuration file 
is required for `transmit`). If you wish to use `generate` however a configuration file
is required. 

    {
      "version": "1",                               # anything you want
      "settings": {
        "api_key": "<YOUR API KEY HERE>"            # Also can be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys
      }
    }

Each command also has its own set of command line options that will need to be provided as well 

## Transmit
UCA data transmission allows you easily send UCA data directly to the CloudZero API without having to write
code. Prepare an input file with one or more correctly formatted JSON UCA records and quickly send it to
the CloudZero telemetry API. 

### Help
    $ uca transmit --help
    Usage: uca transmit [OPTIONS]
    
    Options:
      -d, --data TEXT       Source data, in text or gzip + text format, supports
                            file:// or s3:// paths  [required]
      -t, --transform TEXT  Optional transformation script using jq
                            (https://stedolan.github.io/jq/). Used when the source
                            data needs modification or cleanup. See README.md for
                            usage instructions
      --help                Show this message and exit.

### input data
Your input data can be either a text or gzip file, consisting of one JSON record per line. 

For example:

     {'timestamp': '2021-03-22 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'StateEx', 'target': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'} 
     {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'cost-context': 'Cost-Per-Fake-Customer', 'id': 'Hooli', 'target': {}, 'telemetry-stream': 'test-data', 'value': '23.0000'}

#### Using an optional JQ transform
You can optionally provide a JQ script to transform the source data on the fly before transmission. 
This is helpful when you have minor or even major changes you want to make to the data quickly, and
it would be more complicated or impossible to alter the input data (for example an existing system
is producing UCA data in an older format).

##### Example JQ Script
The following script requires the `id` field to be present (records missing this field will be skipped), followed
by setting the target field using a metadata and cost-context field, followed by setting the cost-context to a 
constant value and then deleting the metadata and uca fields

    select(.id != "")
    | .target = {"tag:environment": [.metadata.environment], "feature": [.["cost-context"]] }
    | .["cost-context"] = "cost-per-title"
    | del(.metadata, .uca)

##### Example Input before JQ transform:
    {
      "uca": "v1.3",
      "timestamp": "2021-05-25 13:00:00+0000",
      "granularity": "HOURLY",
      "context": "rosebud",
      "id": "frank",
      "target": {},
      "telemetry-stream": "test-data",
      "value": "1073641",
      "metadata": {
        "environment": "production"
      }
    }

##### Example Transformed Output after JQ transform:
    {
      "timestamp": "2021-05-25 13:00:00",
      "granularity": "HOURLY",
      "context": "Cost-Per-Customer",
      "id": "frank",
      "target": {
        "tag:environment": ["production"],
        "feature": ["rosebud"]
      },
      "telemetry-stream": "test-data",
      "value": "1073641"
    }

## Generate
Generates UCA data from a source data set (in CSV format) or just based on rules you define. The time period
for the data can be defined as part of the source data or generated based on a start and end range

### Help
    $ uca generate --help
    Usage: uca generate [OPTIONS]
    
    Options:
      -s, --start TEXT  start datetime <YYYY-MM-DD HH:MM:SS> (optional)
      -e, --end TEXT    End datetime <YYYY-MM-DD HH:MM:SS> (optional)
      --today           Generate events for the current day (optional)
      -d, --data TEXT   Input UCA data (CSV)  [required]
      --help            Show this message and exit.

#### Examples
Generate UCA data between 2021-03-13 and 2021-04-07 using data/configuration.json and data/data.csv as input. 
Performs only a dry run and do not send the results to the CloudZero API

    $ uca generate -s 2021-03-13 -e 2021-04-07 -c data/configuration.json -d data/data.csv --dry-run

Generate UCA data using data/configuration.json and data/data.csv (which must contain a timestamp column) 
as input. Performs only a dry run and do not send the results to the CloudZero API

    $ uca generate -s 2021-03-13 -e 2021-04-07 -c data/configuration.json -d data/data.csv --dry-run


#### Configuration File
The `generate` command requires a UCA template definition and specific settings that should be applied when generating data. You 
can learn more [about the UCA format and our UCA Telemetry API here](https://docs.cloudzero.com/reference#telemetry).

    {
      "version": "1",                               # can be anything you want that helps you keep track of things
      "template": {
        "timestamp": "$timestamp",                  # Timestamp will be replaced automatically or from the input data source
        "granularity": "DAILY",                     # Granularity can be HOURLY, DAILY or MONTHLY. See notes below for usage
        "context": "Cost-Per-Fake-Customer",   # You can have up to 5 telemetry streams per context
        "id": "$unit_id",                           # Will be replaced using data from your data CSV
        "target": {},                               # Use {} to map to all spend or use a combination of tags and keywords to get more specific
        "telemetry-stream": "test-data",            # Unique name for this telemetry stream          
        "value": "$unit_value"                      # Will be replaced using generated data or data from your data CSV
      },
      "settings": {
        "generate": {
          "mode": "exact",                            # Can be exact, random, jitter or allocation
          "jitter": 15,                               # if mode is jitter, this value defines the range
          "allocation": 100000                        # if mode is allocation, this value defines the total amount to be allocated
        },
        "api_key": "<YOUR API KEY HERE>"            # Also can be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys
      }
    }

##### A note on using MONTHLY granularity.
MONTHLY is a special granularity that when used instructs the UCA toolkit to expand the provided year and month
to all possible days in the current month. For example if you have this input data:

     unit_id,granularity,timestamp,unit_value
     "SuperDogs, Inc",Monthly,2022-10-1,8
     "CoolCats, LLC",Monthly,2022-10-1,229

This will expand to 61 events, 31 for "SuperDogs, Inc" and 31 for "CoolCats, LLC" (31 days in October) 

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

    {'timestamp': '2021-03-22 00:00:00+00:00', 'granularity': 'DAILY', 'context': 'Cost-Per-Fake-Customer', 'id': 'StateEx', 'target': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'context': 'Cost-Per-Fake-Customer', 'id': 'Hooli', 'target': {}, 'telemetry-stream': 'test-data', 'value': '23.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'context': 'Cost-Per-Fake-Customer', 'id': 'Sunbank', 'target': {}, 'telemetry-stream': 'test-data', 'value': '37.0000'}
    {'timestamp': '2021-04-06 00:00:00+00:00', 'granularity': 'DAILY', 'context': 'Cost-Per-Fake-Customer', 'id': 'Transport Co.', 'target': {}, 'telemetry-stream': 'test-data', 'value': '25.0000'}
    {'timestamp': '2021-03-19 00:00:00+00:00', 'granularity': 'DAILY', 'context': 'Cost-Per-Fake-Customer', 'id': 'StateEx', 'target': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}