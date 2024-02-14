#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import sys
from math import ceil

import requests
from requests import HTTPError

from uca.common.formatters import chunks
from uca.constants import UCA_API_BATCH_SIZE


def send_uca_events(api_key, uca_events, telemetry_type="allocation"):
    print(
        f"Sending {len(uca_events)} {telemetry_type} events to UCA API in {max(ceil(len(uca_events) / UCA_API_BATCH_SIZE), 1)} transaction(s)"
    )

    if telemetry_type == "allocation":
        url = f"https://api.cloudzero.com/unit-cost/v1/telemetry/allocation/{uca_events[0]['telemetry-stream']}"
    else:
        url = f"https://api.cloudzero.com/unit-cost/v1/telemetry/metric/{uca_events[0]['metric-name']}"

    for chunk in chunks(uca_events, UCA_API_BATCH_SIZE):
        payload = {"records": chunk}
        headers = {"Authorization": api_key, "Content-Type": "application/json"}
        try:
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            print(".", end="", flush=True)
        except HTTPError as error:
            print(error)
            print(response.text)
            sys.exit(-1)
    print("Done!")
