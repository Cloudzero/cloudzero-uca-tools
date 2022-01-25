# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import calendar
import sys
from datetime import timedelta
from decimal import Decimal
from random import randint
from string import Template

import simplejson as json

from uca.common.cli import eprint
from uca.common.custom_types import TimeRange
from uca.common.standards import datetime_chunks, utc_datetime_from_anything

PRECISION = 10000


def generate_uca(time_range: TimeRange, uca_template, settings, data_file):
    expand_month = False
    if uca_template['granularity'] == "HOURLY":
        delta = timedelta(hours=1)
    elif uca_template['granularity'] == "DAILY":
        delta = timedelta(days=1)
    elif uca_template['granularity'] == "MONTHLY":
        delta = timedelta(days=1)
        uca_template['granularity'] = "DAILY"
        expand_month = True
    else:
        eprint(f"Granularity {uca_template['granularity']} not supported")
        sys.exit(-1)

    uca_data = data_file
    uca_events = []
    template = Template(json.dumps(uca_template))
    if time_range:
        for timestamp in datetime_chunks(time_range.start, time_range.end, delta):
            uca_events += _render_uca_data(uca_data, settings, template, timestamp)
    else:
        if expand_month:
            for row in uca_data:
                start_date = utc_datetime_from_anything(row['timestamp']).replace(day=1, hour=0, minute=0,
                                                                                  second=0, microsecond=0)
                end_date = start_date.replace(day=calendar.monthrange(year=start_date.year, month=start_date.month)[1])
                time_range = TimeRange(start=start_date, end=end_date)
                for timestamp in datetime_chunks(time_range.start, time_range.end, delta):
                    uca_events += _render_uca_data([row], settings, template, timestamp)
        else:
            uca_events = _render_uca_data(uca_data, settings, template)
    return uca_events


def _render_uca_data(uca_data, settings, template, timestamp=None):
    uca_events = []
    for row in uca_data:
        if settings['mode'] == 'random':
            unit_value = preserve_precision(row['unit_value'], PRECISION)
            row['unit_value'] = str(restore_precision(randint(0, unit_value), PRECISION))
        if settings['mode'] == 'jitter':
            jitter = int(settings['jitter'])
            row['unit_value'] = str(
                round_decimal(max(Decimal(abs(Decimal(row['unit_value']) + randint(-jitter, jitter))), Decimal(1)),
                              PRECISION))
        elif settings['mode'] == 'allocation':
            row['unit_value'] = round_decimal(Decimal(settings['allocation']) * Decimal(row['unit_allocation']),
                                              PRECISION)
        elif settings['mode'] == 'exact':
            row['unit_value'] = str(round_decimal(Decimal(row['unit_value']), PRECISION))
        else:
            eprint(
                f"Unsupported UCA Mode '{settings['mode']}', please choose either 'exact', 'random', 'jitter' or 'allocation'")
            sys.exit(-1)
        if timestamp:
            rendered_template = template.substitute({**row, timestamp: timestamp})
        else:
            rendered_template = template.substitute(**row)
        uca_events.append(json.loads(rendered_template.strip().replace("\n", "")))
    return uca_events


def round_decimal(input_number: Decimal, precision):
    return input_number.quantize(Decimal(f"1.{(len(str(precision)) - 1) * '0'}"))


def preserve_precision(input_number: (str, int, Decimal), precision: int):
    return int(round_decimal(Decimal(input_number), precision) * precision)


def restore_precision(input_number: (str, int, Decimal), precision: int):
    return round_decimal(Decimal(input_number / precision), precision)
