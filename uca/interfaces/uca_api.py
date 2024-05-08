#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import sys
from math import ceil

import requests
from requests import HTTPError

from uca.common.formatters import chunks
from uca.constants import UCA_API_BATCH_SIZE


def send_uca_events(stream_name, stream_type, transmit_type, api_key, uca_events):
    """
    Send UCA events to the UCA API

    Args:
    ----
        stream_name:
        stream_type:
        transmit_type:
        api_key:
        uca_events:

    Returns:
    -------
        None

    """
    print(
        f"Sending {len(uca_events)} {stream_type} events to {transmit_type.upper()} UCA API in {max(ceil(len(uca_events) / UCA_API_BATCH_SIZE), 1)} transaction(s)"
    )

    url = f"https://api.cloudzero.com/unit-cost/v1/telemetry/{stream_type}/{stream_name}/{transmit_type}"

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
