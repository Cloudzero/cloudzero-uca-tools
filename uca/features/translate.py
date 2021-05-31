# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import sys
from collections import defaultdict, Counter
import re
import simplejson as json
from string import Template

from aws_log_parser import log_parser, LogType

from uca.common.cli import eprint
from uca.common.formatters import rgetattr


def translate(input_data, format, configuration):
    uca_data = defaultdict()
    uca_values = Counter()

    if format.lower() == "elb":
        log_type = LogType.ClassicLoadBalancer
    elif format.lower() == "alb":
        log_type = LogType.LoadBalancer
    elif format.lower() == "cloudfront":
        log_type = LogType.LoadBalancer
    else:
        eprint(f"Unsupported log type {format}, valid choices are ELB, ALB or CloudFront")
        sys.exit(1)

    entries = log_parser(input_data, log_type)
    template = Template(json.dumps(configuration.template))
    pattern = re.compile(configuration.settings['unit_id_translate_field_regex'], re.IGNORECASE)
    for entry in entries:
        unit_id_root_value = rgetattr(entry, configuration.settings['unit_id_translate_field'])
        regex_match = pattern.search(unit_id_root_value)
        if regex_match and regex_match.group():
            unit_id_root_value = regex_match.group()
            raw_entry = vars(entry)
            raw_entry['timestamp'] = transform_timestamp(entry.timestamp, configuration)
            value_index = f"{raw_entry['timestamp']}-{unit_id_root_value}"
            uca_values[value_index] += 1
            rendered_template = template.substitute(**raw_entry,
                                                    unit_value=uca_values[value_index],
                                                    unit_id=unit_id_root_value)
            uca_data[value_index] = rendered_template

    return list(uca_data.values())


def transform_timestamp(timestamp, configuration):
    if configuration.granularity == "DAILY":
        return timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
    elif configuration.granularity == "HOURLY":
        return timestamp.replace(minute=0, second=0, microsecond=0)
    else:
        eprint(f"Unsupported granularity {configuration.granularity}")
        sys.exit()