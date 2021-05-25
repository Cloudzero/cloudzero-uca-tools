# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

from datetime import datetime, timezone
from typing import Optional, Any

import dateutil.parser as parser


def utc_datetime_from_anything(input_data: Any) -> Optional[datetime]:
    if input_data is None:
        return None

    if isinstance(input_data, datetime):
        parsed_datetime = input_data
    elif isinstance(input_data, str):
        parsed_datetime = parser.parse(input_data)
    else:
        # if it's larger than the max size for a 32 bit integer it's in ms
        if input_data > 2147483647:
            input_data /= 1000
        parsed_datetime = datetime.fromtimestamp(input_data, tz=timezone.utc)

    if parsed_datetime.tzinfo is None:
        return parsed_datetime.replace(tzinfo=timezone.utc)
    else:
        return parsed_datetime.astimezone(tz=timezone.utc)


def datetime_chunks(start, end, delta):
    """
    set delta to something like timedelta(hours=1)

    Args:
        start:
        end:
        delta:

    Returns:

    """
    datetime_chunk = start
    while datetime_chunk + delta <= end:
        yield datetime_chunk
        datetime_chunk += delta
