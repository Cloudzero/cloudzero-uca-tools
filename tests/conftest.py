#  Copyright (c) 2024 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

def input_uca_data():
    """
    Return input uca data fixture

    Returns
    -------
        list

    """
    return [
        {"unit_id": "Sunbank", "unit_value": "0"},
        {"unit_id": "SoftwareCorp", "unit_value": "0"},
        {"unit_id": "Parts, Inc.", "unit_value": "0"},
        {"unit_id": "Transport Co.", "unit_value": "0"},
        {"unit_id": "WeShipit, Inc.", "unit_value": "0"},
        {"unit_id": "CapitalTwo", "unit_value": "0"},
        {"unit_id": "Bank of Sokovia", "unit_value": "0"},
        {"unit_id": "Makers", "unit_value": "0"},
        {"unit_id": "StateEx", "unit_value": "0"},
        {"unit_id": "Flitter", "unit_value": "0"},
        {"unit_id": "Pets2you", "unit_value": "0"},
        {"unit_id": "Hooli", "unit_value": "0"},
        {"unit_id": "Massive Dynamic", "unit_value": "1000"},
    ]


def input_settings():
    """
    Return input settings fixture

    Returns
    -------
        dict

    """
    return {
        "stream_name": "test-data",
        "stream_type": "allocation",
        "generate": {"allocation": "", "jitter": "", "mode": "exact"},
    }


def input_template():
    """
    Return input template fixture

    Returns
    -------
        dict

    """
    return {
        "granularity": "DAILY",
        "id": "$unit_id",
        "target": {},
        "timestamp": "$timestamp",
        "value": "$unit_value",
    }
