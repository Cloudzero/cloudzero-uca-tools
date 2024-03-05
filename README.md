# CloudZero UCA Toolkit
Utilities for generating, transforming and transmitting unit cost analytics (UCA) data to the CloudZero API.
Visit our [UCA documentation](https://docs.cloudzero.com/docs/unit-cost-analytics) to learn more about
[CloudZero](https://www.cloudzero.com) and our enhanced unit cost analytics capabilities.

## Features
* Transmit UCA data to CloudZero (using the CloudZero UCA API)
* Generate UCA data
* Convert raw data in CSV form to UCA JSON format

## Prerequisites
* Tested on MacOS, should probably run on Linux in general
* Python 3.9 or newer
* `pipx` or your favorite method of installing packages from PyPi. Have you considered [pipx](https://pypa.github.io/pipx/)?

## Installation
      $ pipx install cloudzero-uca-tools

## Quick Starts

* [Allocation Telemetry Quick Start](docs/quick_starts/quick_start_allocation_telemetry/quick_start_allocation_telemetry.md)
* [Unit Metric Telemetry Quick Start](docs/quick_starts/quick_start_unit_metric_telemetry/quick_start_unit_metric_telemetry.md)

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
      -dry, --dry-run           Perform a dry run, read and transform the data but
                                do not send it to the API. Sample events will be output to the screen
      -k, --api-key TEXT        API Key to use
      --help                    Show this message and exit.
    
    Commands:
      convert
      transmit
      generate

### Basic Configuration
A configuration file is typically required to define how UCA telemetry is to be created, converted or transmitted.
The following is a minimal configuration file for transmitting data to the CloudZero API 
(if you don't want to specify the API on the command line, otherwise no configuration file 
is required for `transmit`). If you wish to use `generate` or `convert` however a configuration file
is required.

    {
      "version": "1",                               
      "settings": {
        "api_key": "<YOUR API KEY HERE>"
      }
    }

    # API Key can also be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys

Each command has its own set of command line options that will need to be provided as well 

## Transmit
`transmit` allows you send UCA data directly to the CloudZero API without having to write
code. To use `transmit` you prepare in advance an [ND-JSON](http://ndjson.org/) formatted input file
which contains one or more correctly formatted JSON UCA records as input. 

### Help
    $ uca transmit --help
    Usage: uca transmit [OPTIONS]
    
    Options:
      -d, --data TEXT       Source data, in text or gzip + text format, supports
                            file:// or s3:// paths  [required]
      -o, --output TEXT     Instead of sending events to the API, write
                            events to an output file (note: will overwrite file if it exists)
      -t, --transform TEXT  Optional transformation script using jq
                            (https://stedolan.github.io/jq/). Used when the source
                            data needs modification or cleanup. See README.md for
                            usage instructions
      --help                Show this message and exit.

### input data
Your input data must be a valid [ND-JSON](http://ndjson.org/) document which can be either a text or gzip file,
consisting of one JSON record per line. 

For example:

     {'timestamp': '2021-03-22 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'StateEx', 'filter': {"custom:Environment": ["Production"]}, 'telemetry-stream': 'test-data', 'value': '40.0000'} 
     {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'Hooli', 'filter': {"custom:Environment": ["Production"]}, 'telemetry-stream': 'test-data', 'value': '23.0000'}

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
    | .filter = {"tag:environment": [.metadata.environment], "tag:feature": [".metadata.feature"] }
    | del(.metadata, .uca)

##### Example Input before JQ transform:
    {
      "uca": "v1.5",
      "timestamp": "2021-05-25 13:00:00+0000",
      "granularity": "HOURLY",
      "element-name": "frank",
      "telemetry-stream": "test-data",
      "value": "1073641",
      "metadata": {
        "environment": "production",
        "feature": "rosebud"
      }
    }

##### Example Transformed Output after JQ transform:
    {
      "timestamp": "2021-05-25 13:00:00",
      "granularity": "HOURLY",
      "id": "frank",
      "filter": {
        "tag:environment": ["production"],
        "tag:feature": ["rosebud"]
      },
      "telemetry-stream": "Cost-Per-Customer",
      "value": "1073641"
    }

## Convert
`convert` allows you to convert raw data in CSV format to UCA JSON format. To use `convert` you prepare in advance a CSV file of the
raw unit cost data you wish to convert and then define the mapping of the CSV columns to UCA fields in a configuration file.

### Help
    $ uca generate --help
    Usage: uca convert [OPTIONS]
    
    Options:
      -d, --data TEXT  Source data, in text or gzip + text format, supports
                       file:// or s3:// paths  [required]
      --help           Show this message and exit.

### Configuration File
    {
      "version": "1",
      "template": {
        "timestamp": "$ACCESS_TIME",
        "granularity": "HOURLY",
        "element-name": "$CUST_ID",
        "filter": {
          "custom:Environment": [
            "Prod"
          ]
        },
        "telemetry-stream": "cost-per-customer",
        "value": "$DURATION"
      },
      "settings": {
        "api_key": "<YOUR API KEY HERE>"            # Also can be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys
        "convert": {
          "stream_name": "cost-per-customer",
          "format": "CSV",                          # currently only CSV is supported
          "schema": {
            "columns": {                            # Define one or more columns that will be used from the input CSV file
              "CUST_ID": {                          # The name of the column in the CSV file
                "type": "STRING"                    # Specify the type of the column to ensure proper conversion, can be STRING, NUMBER, DATETIME or TIME
              },
              "ACCESS_TIME": {
                "type": "DATETIME"                  # DATETIME is a special type that will attempt to convert a wide range of datetime formats (including unix timestamp) to ISO 8601 UTC format 
              },
              "DURATION": {
                "type": "TIME",                     # TIME is a special type that will convert a time duration expressed in HH:mm:ss to seconds
                "format": "HH:mm:ss"
              }
            }
          }
        }
      }
    }

#### Examples
Convert raw data from `data-file.csv` into UCA JSON format using a `config-file.json` as configuration, and write to `output-file.json`

    $ uca convert -d data-file.csv -c config-file.json -o output-file.json 


## Generate
`generate` will create UCA data over a defined time period based on rules and source data (CSV) that you define.
Rules enable you to define how the data is to be generated based on the provided source data and can be used to 
create static allocations, dynamic allocations, or even random allocations that can be used to verify system operation
or facilitate a demonstration.

### Help
    $ uca generate --help
    Usage: uca generate [OPTIONS]
    
    Options:
      -s, --start TEXT   start datetime <YYYY-MM-DD HH:MM:SS>                      [optional]
      -e, --end TEXT     End datetime <YYYY-MM-DD HH:MM:SS>                        [optional]
      --today            Generate events for the current day                       [optional]
      -d, --data TEXT    Input UCA data (CSV)                                      [required]
      -o, --output TEXT  Instead of transmitting the data to the CloudZero API,    [optional]
                         Save the output to a file.
      --help             Show this message and exit.                               [optional]

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
        "element-name": "$element_name",            # Will be replaced using data from your data CSV
        "filter": {},                               # Use a filter to map spend to a combination of tags, dimensions, accounts, etc...
        "telemetry-stream": "test-data",            # Unique name for this telemetry stream          
        "value": "$value"                           # Will be replaced using generated data or data from your data CSV
      },
      "settings": {
        "generate": {
          "mode": "exact",                          # Can be `exact`, `random`, `jitter` or `allocation`
          "jitter": 15,                             # if mode is jitter, defines the +/- random range to applie to the $value
          "allocation": 1000                        # if mode is allocation, defines the total amount to be allocated across elements in your data file
          "precision": 4                            # The number of desired decimal places. If not provided, the default is 4
        },
        "api_key": "<YOUR API KEY HERE>"            # Also can be provided at runtime via the CLI. Get an API key at https://app.cloudzero.com/organization/api-keys
      }
    }

##### A note on using MONTHLY granularity.
MONTHLY is a special (non-standard) granularity that can only be used with the UCA toolkit. MONTHLY will expand the input data 
over the year and month provided to all possible days in a given month to create DAILY UCA telemetry.

For example if you have this input data:

     element_name,timestamp,value
     "SuperDogs, Inc",2022-10-1,8
     "CoolCats, LLC",2022-10-1,229

This will expand to 61 events, 31 for "SuperDogs, Inc" and 31 for "CoolCats, LLC" (31 days in October) 

#### Data CSV
The data CSV defines the input data you wish to feed into the template to produce
matching UCA records for all rows in your data CSV for each hour or day as defined. The following
example has 13 "customers" and can be used as input for all configuration modes (`exact`, `random`, `jitter`, or `allocation`).

        element_name,value,allocation
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
Using the `exact` configuration above, this data will produce UCA events similar to the following:

    {'timestamp': '2021-03-22 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'StateEx', 'filter': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'Hooli', 'filter': {}, 'telemetry-stream': 'test-data', 'value': '23.0000'}
    {'timestamp': '2021-04-01 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'Sunbank', 'filter': {}, 'telemetry-stream': 'test-data', 'value': '37.0000'}
    {'timestamp': '2021-04-06 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'Transport Co.', 'filter': {}, 'telemetry-stream': 'test-data', 'value': '25.0000'}
    {'timestamp': '2021-03-19 00:00:00+00:00', 'granularity': 'DAILY', 'element-name': 'StateEx', 'filter': {}, 'telemetry-stream': 'test-data', 'value': '40.0000'}

## Testing/Developing
First create a virtual environment of your choice, and activate it. Then, install UCA Toolkit for local development:
```bash
python -m pip install --editable .
```
Run the following commands if you had previously installed it using pip or pipx:

1. Uninstall `uca` (e.g. pipx uninstall cloudzero-uca-tools)
2. Create a Virtualenv for your `uca` development
3. Enter your virtualenv and install all of the necessary dependencies by running make init
4. Finally, configure `uca` for use in your environment using pip install -e .
5. Once that is done, the `uca` cli will be available in your shell (you may or may not need to restart your shell).