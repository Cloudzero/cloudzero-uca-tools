#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com


from datetime import datetime, timezone
from typing import Any, Optional

import dateutil.parser as parser

from uca.exceptions import InvalidDate


def get_seconds_from_time(time_str):
    """
    Get seconds from time.
    """
    h, m, s = time_str.split(":")
    return int(h) * 3600 + int(m) * 60 + int(s)


def utc_datetime_from_anything(input_data: Any) -> Optional[datetime]:
    """
    Convert a variety of input data types to a UTC datetime object

    Args:
    ----
        input_data:

    Returns:
    -------
        datetime

    """
    if input_data is None:
        return None
    try:
        if isinstance(input_data, datetime):
            parsed_datetime = input_data
        elif isinstance(input_data, str):
            parsed_datetime = parser.parse(input_data)
        else:
            # if it's larger than the max size for a 32-bit integer it's in ms
            if input_data > 2147483647:
                input_data /= 1000
            parsed_datetime = datetime.fromtimestamp(input_data, tz=timezone.utc)
        if parsed_datetime.tzinfo is None:
            return parsed_datetime.replace(tzinfo=timezone.utc)
        else:
            return parsed_datetime.astimezone(tz=timezone.utc)
    except parser.ParserError as error:
        raise InvalidDate(error) from error


def datetime_chunks(start, end, delta):
    """
    Set delta to something like timedelta(hours=1)

    Args:
    ----
        start:
        end:
        delta:

    Returns:
    -------
        None

    """
    datetime_chunk = start
    while datetime_chunk + delta <= end:
        yield datetime_chunk
        datetime_chunk += delta


def valid_settings(settings):
    """
    Validate settings

    Args:
    ----
        settings:

    Returns:
    -------
        bool

    """
    required_settings_keys = {"stream_type", "stream_name", "generate"}
    missing_keys = required_settings_keys - set(settings.keys())

    if missing_keys:
        raise KeyError(f"Missing required key(s) in Settings: {', '.join(missing_keys)}")

    stream_type_values = {"allocation", "metric"}
    if settings["stream_type"].lower() not in stream_type_values:
        raise ValueError(f"Stream Type must be {' or '.join(stream_type_values)}")

    if "transmit_type" in settings:
        transmit_type_values = {"sum", "replace", "delete", "update"}
        if settings["transmit_type"].lower() not in transmit_type_values:
            raise ValueError(f"Transmit Type must be {' or '.join(transmit_type_values)}")

    if not isinstance(settings["generate"], dict):
        raise TypeError("Generate settings must be a dictionary")

    required_generate_keys = {"mode"}
    missing_keys = required_generate_keys - set(settings["generate"].keys())

    if missing_keys:
        raise KeyError(f"Missing required key(s) in Generate settings: {', '.join(missing_keys)}")

    return True


def valid_template(template, stream_type):
    """
    Validate template

    Args:
    ----
        template:
        stream_type:

    Returns:
    -------
        bool

    """
    if stream_type == "allocation":
        required_template_keys = {
            "granularity",
            "element_name",
            "filter",
            "value",
            "timestamp",
        }

    elif stream_type == "metric":
        required_template_keys = {
            "associated_cost",
            "value",
            "timestamp",
        }

    missing_keys = required_template_keys - set(template.keys())
    extra_keys = set(template.keys()) - required_template_keys

    if missing_keys:
        raise KeyError(f"Missing required key(s) in Template: {', '.join(missing_keys)}")

    if extra_keys:
        raise KeyError(f"Extra key(s) present in Template: {', '.join(extra_keys)}")

    if stream_type == "allocation":
        granularity_values = {"hourly", "daily", "monthly"}
        if template["granularity"].lower() not in granularity_values:
            raise ValueError(f"Granularity must be {' or '.join(granularity_values)}")

        if not isinstance(template["filter"], dict):
            raise TypeError("filter must be a dictionary")

    elif stream_type == "metric":
        if not isinstance(template["associated_cost"], dict):
            raise TypeError("associated_cost must be a dictionary")

    return True
