# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import sys
from math import ceil

import requests
from requests import HTTPError

from uca.common.formatters import chunks
from uca.constants import UCA_API_BATCH_SIZE


def send_uca_events(api_key, uca_events):
    print(
        f"Sending {len(uca_events)} events to UCA API in {max(ceil(len(uca_events) / UCA_API_BATCH_SIZE), 1)} transaction(s)")
    for chunk in chunks(uca_events, UCA_API_BATCH_SIZE):
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
            print(error)
            print(response.text)
            sys.exit(-1)
    print("Done!")
