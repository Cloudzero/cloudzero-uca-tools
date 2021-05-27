# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import sys
from datetime import timedelta
from decimal import Decimal
from random import randint
from string import Template

import simplejson as json

from uca.common.cli import eprint
from uca.common.custom_types import TimeRange
from uca.common.standards import datetime_chunks

PRECISION = 10000


def generate_uca(time_range: TimeRange, uca_template, uca_settings, data_file):
    template = Template(json.dumps(uca_template))

    if uca_template['granularity'] == "HOURLY":
        delta = timedelta(hours=1)
    elif uca_template['granularity'] == "DAILY":
        delta = timedelta(days=1)
    else:
        print(f"Granularity {uca_template['granularity']} not supported")
        sys.exit(-1)

    uca_data = list(data_file)
    uca_events = []
    for timestamp in datetime_chunks(time_range.start, time_range.end, delta):
        for row in uca_data:
            if uca_settings['mode'] == 'random':
                unit_value = preserve_precision(row['unit_value'], PRECISION)
                row['unit_value'] = str(restore_precision(randint(0, unit_value), PRECISION))
            if uca_settings['mode'] == 'jitter':
                jitter = int(uca_settings['jitter'])
                row['unit_value'] = str(round_decimal(Decimal(abs(Decimal(row['unit_value']) + randint(-jitter, jitter))), PRECISION))
            elif uca_settings['mode'] == 'allocation':
                row['unit_value'] = round_decimal(Decimal(uca_settings['allocation'] * row['unit_allocation']), PRECISION)
            elif uca_settings['mode'] == 'exact':
                row['unit_value'] = str(round_decimal(Decimal(row['unit_value']), PRECISION))
            else:
                eprint(f"Unsupported UCA Mode '{uca_settings['mode']}', please choose either 'exact', 'random', 'jitter' or 'allocation'")
                sys.exit(-1)
            rendered_template = template.substitute(**row, timestamp=timestamp)
            uca_events.append(json.loads(rendered_template.strip().replace("\n", "")))

    return uca_events


def round_decimal(input_number: Decimal, precision):
    return input_number.quantize(Decimal(f"1.{(len(str(precision)) - 1) * '0'}"))


def preserve_precision(input_number: (str, int, Decimal), precision: int):
    return int(round_decimal(Decimal(input_number), precision) * precision)


def restore_precision(input_number: (str, int, Decimal), precision: int):
    return round_decimal(Decimal(input_number / precision), precision)
