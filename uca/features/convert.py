#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import re
import sys
from collections import Counter, defaultdict
from decimal import Decimal
from string import Template

import simplejson as json

from uca.common.cli import eprint
from uca.common.formatters import rgetattr
from uca.common.standards import get_seconds_from_time, utc_datetime_from_anything
from uca.vendored.aws_log_parser import AwsLogParser, LogType

AWS_FORMAT_TYPE = "AWS"
CSV_FORMAT_TYPE = "CSV"


def transform_csv_record(record, configuration):
    """
    Transform a CSV record

    Args:
    ----
        record:
        configuration:

    Returns:
    -------
        record

    """
    schema = configuration.settings["convert"]["schema"]["columns"]
    for column_name, value in record.items():
        if schema.get(column_name):
            try:
                if schema[column_name]["type"] == "TIME":
                    record[column_name] = get_seconds_from_time(value)
                if schema[column_name]["type"] == "DATETIME":
                    record[column_name] = utc_datetime_from_anything(value).isoformat()
                if schema[column_name]["type"] == "NUMBER":
                    record[column_name] = Decimal(value)
            except Exception as error:
                eprint(f"Error transforming {column_name} with value {value}: {error}")
                sys.exit(1)
    return record


def zero_values_detected(record):
    """
    Check if a record has zero values

    Args:
    ----
        record:

    Returns:
    -------
        bool

    """
    if Decimal(record["value"]) == 0:
        return True
    return False


def convert(input_data, configuration):
    """
    Convert input data

    Args:
    ----
        input_data:
        configuration:

    Returns:
    -------
        list

    """
    uca_records = []
    uca_data = defaultdict()
    uca_values = Counter()
    data_format = configuration.settings["convert"]["format"].upper()

    if data_format == "CSV":
        format_type = CSV_FORMAT_TYPE
        log_type = None
    elif data_format == "ELB":
        format_type = AWS_FORMAT_TYPE
        log_type = LogType.ClassicLoadBalancer
    elif data_format == "ALB":
        format_type = AWS_FORMAT_TYPE
        log_type = LogType.LoadBalancer
    elif data_format == "CLOUDFRONT":
        format_type = AWS_FORMAT_TYPE
        log_type = LogType.CloudFront
    else:
        eprint(f"Unsupported format {data_format}, valid choices are CSV, ELB, ALB or CLOUDFRONT")
        sys.exit(1)

    template = Template(json.dumps(configuration.template))
    settings = configuration.settings["convert"]

    if format_type == AWS_FORMAT_TYPE:
        parser = AwsLogParser(log_type)
        entries = parser.parse(content=input_data)  # TODO move this to read_url
        unit_id_settings = settings["unit_id"]
        pattern = re.compile(unit_id_settings["regex"], re.IGNORECASE)
        for entry in entries:
            unit_id_attribute = rgetattr(entry, unit_id_settings["attribute"])
            regex_match = pattern.match(unit_id_attribute)
            if regex_match:
                unit_id_value = unit_id_settings["delimiter"].join(regex_match.groups())
                raw_entry = vars(entry)
                raw_entry["timestamp"] = transform_timestamp(entry.timestamp, configuration)
                value_index = f"{raw_entry['timestamp']}-{unit_id_value}"
                uca_values[value_index] += 1
                rendered_template = template.substitute(
                    **raw_entry, unit_value=uca_values[value_index], unit_id=unit_id_value
                )
                uca_data[value_index] = rendered_template
        uca_records = list(uca_data.values())
    elif format_type == CSV_FORMAT_TYPE:
        for record in input_data:
            transformed_record = transform_csv_record(record, configuration)
            if not transformed_record:
                print("B", end="", flush=True)
                continue
            rendered_template = template.substitute(**transformed_record)
            if zero_values_detected(json.loads(rendered_template)):
                print("0", end="", flush=True)
                continue
            uca_records.append(rendered_template)
            print(".", end="", flush=True)

    return uca_records


def transform_timestamp(timestamp, configuration):
    """
    Transform a timestamp

    Args:
    ----
        timestamp:
        configuration:

    Returns:
    -------
        timestamp

    """
    if configuration.granularity == "DAILY":
        return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    elif configuration.granularity == "HOURLY":
        return timestamp.replace(minute=0, second=0, microsecond=0)
    else:
        eprint(f"Unsupported granularity {configuration.granularity}")
        sys.exit()
