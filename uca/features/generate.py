#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import calendar
import copy
import sys
from datetime import timedelta
from decimal import Decimal
from random import randint
from string import Template

import simplejson as json

from uca.common.cli import eprint
from uca.common.custom_types import TimeRange
from uca.common.standards import datetime_chunks, utc_datetime_from_anything

PRECISION = 4


def generate_uca(time_range: TimeRange, uca_template, settings, uca_data) -> list:
    """
    Generate UCA data

    Args:
    ----
        time_range:
        uca_template:
        settings:
        uca_data:

    Returns:
    -------
        uca_events: list

    """
    expand_month = False

    if settings.get("stream_type") == "metric":
        delta = timedelta(days=1)

    else:
        if uca_template["granularity"] == "HOURLY":
            delta = timedelta(hours=1)
        elif uca_template["granularity"] == "DAILY":
            delta = timedelta(days=1)
        elif uca_template["granularity"] == "MONTHLY":
            delta = timedelta(days=1)
            uca_template["granularity"] = "DAILY"
            expand_month = True
        else:
            eprint(f"Granularity {uca_template['granularity']} not supported")
            sys.exit(-1)

    uca_events = []
    if time_range:
        for timestamp in datetime_chunks(time_range.start, time_range.end + timedelta(days=1), delta):
            uca_events += _render_uca_data(uca_data, settings, uca_template, timestamp)

    else:
        unit_value_header = uca_template["value"].replace("$", "")
        timestamp_header = uca_template["timestamp"].replace("$", "")

        if expand_month:
            for row in uca_data:
                if Decimal(row[unit_value_header]) <= 0:
                    continue

                elif not row[timestamp_header]:
                    print("Source data MUST include a timestamp value if no start and end time is provided")

                start_date = utc_datetime_from_anything(row[timestamp_header]).replace(
                    day=1, hour=0, minute=0, second=0, microsecond=0
                )
                end_date = start_date.replace(day=calendar.monthrange(year=start_date.year, month=start_date.month)[1])
                for timestamp in datetime_chunks(start_date, end_date + timedelta(days=1), delta):
                    single_row = copy.deepcopy(row)
                    uca_events += _render_uca_data([single_row], settings, uca_template, timestamp)
        else:
            uca_events = _render_uca_data(uca_data, settings, uca_template)

    return uca_events


def _render_uca_data(uca_data, settings, uca_template, timestamp=None):
    """
    Render UCA data

    Args:
    ----
        uca_data:
        settings:
        uca_template:
        timestamp:

    Returns:
    -------
        list

    """
    generate_settings = settings.get("generate")
    unit_value_header = uca_template["value"].replace("$", "")
    timestamp_header = uca_template["timestamp"].replace("$", "")

    try:
        precision = int("1" + "0" * int(settings.get("precision", PRECISION)))

    except TypeError:
        print("precision is Settings must be an integer")
        sys.exit(-1)
    except ValueError:
        print("precision is Settings must be an integer")
        sys.exit(-1)

    uca_events = []
    # skipped = 0
    for row in uca_data:
        try:
            if not row[unit_value_header] or Decimal(row[unit_value_header]) <= 0:
                continue
        except Exception as err:
            print(f"Error: {err}")
            print(f"{row[unit_value_header]}")
            sys.exit(-1)

        if generate_settings.get("mode") == "random":
            unit_value = preserve_precision(row[unit_value_header], precision)
            row[unit_value_header] = str(restore_precision(randint(0, unit_value), precision))
        elif generate_settings.get("mode") == "jitter":
            jitter = int(generate_settings.get("jitter"))
            row[unit_value_header] = str(
                round_decimal(
                    max(Decimal(abs(Decimal(row[unit_value_header]) + randint(-jitter, jitter))), Decimal(1)), precision
                )
            )
        elif generate_settings.get("mode") == "allocation":
            jitter = None
            if generate_settings.get("jitter"):
                jitter = int(generate_settings.get("jitter"))
            try:
                if jitter:
                    row[unit_value_header] = round_decimal(
                        (Decimal(settings["allocation"]) * Decimal(row["unit_allocation"])) + randint(0, jitter),
                        precision,
                    )
                else:
                    row[unit_value_header] = round_decimal(
                        Decimal(settings["allocation"]) * Decimal(row[unit_value_header]), precision
                    )

            except KeyError:
                print('ERROR: Must add "unit_allocation" column to CSV')
                sys.exit(-1)
            except Exception as error:
                print(f"ERROR: {error}")
                sys.exit(-1)

        elif generate_settings.get("mode") == "exact":
            row[unit_value_header] = str(round_decimal(Decimal(row[unit_value_header]), precision))
        else:
            eprint(
                f"Unsupported UCA Mode '{generate_settings.get('mode')}', please choose either 'exact', 'random', 'jitter' or 'allocation'"
            )
            sys.exit(-1)

        try:
            template = Template(json.dumps(uca_template))
            if timestamp:
                rendered_template = template.substitute({**row, timestamp_header: timestamp})

            else:
                rendered_template = template.substitute(**row)

            uca_events.append(json.loads(rendered_template.strip().replace("\n", "")))

        except KeyError as err:
            print(f"Missing key in CSV data: {err}")
            sys.exit(-1)
        except Exception as err:
            print(f"Error: {err}")
            print(row)
            sys.exit(-1)

    return uca_events


def round_decimal(input_number: Decimal, precision) -> Decimal:
    """
    Round a decimal to a given precision

    >>> round_decimal(Decimal('1.23456789'), 100)
    Decimal('1.23')
    >>> round_decimal(Decimal(1.23456789), 100)
    Decimal('1.23')

    Args:
    ----
        input_number:
        precision:

    Returns:
    -------
        Decimal

    """
    return input_number.quantize(Decimal(f"1.{(len(str(precision)) - 1) * '0'}"))


def preserve_precision(input_number: (str, int, Decimal), precision: int) -> int:
    """
    Preserve the precision of a number

    Args:
    ----
        input_number:
        precision:

    Returns:
    -------
        int

    """
    return int(round_decimal(Decimal(input_number), precision) * precision)


def restore_precision(input_number: (str, int, Decimal), precision: int) -> int:
    """
    Restore the precision of a number

    Args:
    ----
        input_number:
        precision:

    Returns:
    -------
        int

    """
    return round_decimal(Decimal(input_number / precision), precision)
