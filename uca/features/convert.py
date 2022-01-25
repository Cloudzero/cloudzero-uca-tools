# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import sys
from collections import defaultdict, Counter
import re
import simplejson as json
from string import Template

from aws_log_parser import AwsLogParser, LogType

from uca.common.cli import eprint
from uca.common.formatters import rgetattr

AWS_FORMAT_TYPE = "AWS"
CSV_FORMAT_TYPE = "CSV"


def convert(input_data, configuration):
    uca_records = []
    uca_data = defaultdict()
    uca_values = Counter()
    data_format = configuration.settings['convert']['format'].upper()

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
    settings = configuration.settings['convert']

    if format_type == AWS_FORMAT_TYPE:
        parser = AwsLogParser(log_type)
        entries = parser.parse(content=input_data)  # TODO move this to read_url
        unit_id_settings = settings['unit_id']
        pattern = re.compile(unit_id_settings['regex'], re.IGNORECASE)
        for entry in entries:
            unit_id_attribute = rgetattr(entry, unit_id_settings['attribute'])
            regex_match = pattern.match(unit_id_attribute)
            if regex_match:
                unit_id_value = unit_id_settings['delimiter'].join(regex_match.groups())
                raw_entry = vars(entry)
                raw_entry['timestamp'] = transform_timestamp(entry.timestamp, configuration)
                value_index = f"{raw_entry['timestamp']}-{unit_id_value}"
                uca_values[value_index] += 1
                rendered_template = template.substitute(**raw_entry,
                                                        unit_value=uca_values[value_index],
                                                        unit_id=unit_id_value)
                uca_data[value_index] = rendered_template
        uca_records = list(uca_data.values())
    elif format_type == CSV_FORMAT_TYPE:
        for record in input_data:
            rendered_template = template.substitute(**record)
            uca_records.append(rendered_template)

    return uca_records


def transform_timestamp(timestamp, configuration):
    if configuration.granularity == "DAILY":
        return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    elif configuration.granularity == "HOURLY":
        return timestamp.replace(minute=0, second=0, microsecond=0)
    else:
        eprint(f"Unsupported granularity {configuration.granularity}")
        sys.exit()
