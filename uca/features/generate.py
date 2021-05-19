# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

import sys
from datetime import timedelta
from pprint import pprint
from random import randrange
from string import Template

import requests
import simplejson as json
from requests import HTTPError

from uca.common.cli import confirm
from uca.common.formatters import chunks
from uca.common.standards import datetime_chunks
from uca.common.types import TimeRange

API_BATCH_SIZE = 3000


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

    event_count = 0
    uca_events = []

    for timestamp in datetime_chunks(time_range.start, time_range.end, delta):
        for row in data:
            rendered_template = template.substitute(**row, granularity=granularity, timestamp=timestamp)
            uca_events.append(json.loads(rendered_template.strip().replace("\n", "")))
            event_count += 1

    print(f"Event Generation complete, {event_count} events created\n")
    print("A few random examples:")
    for x in range(5):
        random_event = randrange(1, event_count)
        print(f"{random_event:7} : {uca_events[random_event]}")
    print("\n")
    if confirm("Ready to start sending events?"):
        print(
            f"Sending {event_count} events to UCA API in {max(round(event_count / API_BATCH_SIZE), 1)} transaction(s)")
        for chunk in chunks(uca_events, API_BATCH_SIZE):
            url = "https://api.cloudzero.com/unit-cost/v1/telemetry"
            payload = {"records": chunk}
            headers = {
                "Authorization": api_key,
                "Content-Type": "application/json"
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                response.raise_for_status()
                print(".", end="", flush=True)
            except HTTPError as error:
                pprint(chunk)
                print(error)
                print(response.text)
                sys.exit(-1)
        print(".Done!")
    else:
        print(f"Event Generation Canceled")

    return
