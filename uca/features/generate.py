# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

import sys
from datetime import timedelta
from random import randrange
from string import Template

import simplejson as json

from uca.common.cli import confirm
from uca.common.standards import datetime_chunks
from uca.common.types import TimeRange
from uca.interfaces.uca_api import send_uca_events


def generate_uca(time_range: TimeRange, template_file, data_file, granularity, api_key):
    template = Template(template_file)

    if granularity == "HOURLY":
        delta = timedelta(hours=1)
    elif granularity == "DAILY":
        delta = timedelta(days=1)
    else:
        print(f"Granularity {granularity} not supported")
        sys.exit(-1)

    data = list(data_file)
    uca_events = []

    for timestamp in datetime_chunks(time_range.start, time_range.end, delta):
        for row in data:
            rendered_template = template.substitute(**row, granularity=granularity, timestamp=timestamp)
            uca_events.append(json.loads(rendered_template.strip().replace("\n", "")))

    print(f"Event Generation complete, {len(uca_events)} events created\n")
    print("A few random examples:")
    for x in range(5):
        random_event = randrange(1, len(uca_events))
        print(f"{random_event:7} : {uca_events[random_event]}")
    print("\n")
    if confirm("Ready to start sending events?"):
        send_uca_events(api_key, uca_events)
    else:
        print(f"Event Generation Canceled")

    return
