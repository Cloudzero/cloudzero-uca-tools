#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import datetime
from pathlib import Path

from uca.common.files import load_data_files
from uca.features.generate import _render_uca_data, generate_uca


def test_filter_nil_unit_values_exact_mode(input_uca_data, input_settings, input_template):
    """
    Test to filter out unit values that are nil in exact mode

    Args:
    ----
        input_uca_data:
        input_settings:
        input_template:

    Returns:
    -------
        None

    """
    input_timestamp = datetime.datetime(2022, 10, 30, 0, 0)

    result = _render_uca_data(input_uca_data, input_settings, input_template, input_timestamp)
    assert len(result) == 1


def test_filter_nil_unit_values_random_mode(input_uca_data, input_settings, input_template):
    """
    Test to filter out unit values that are nil in random mode

    Args:
    ----
        input_uca_data:
        input_settings:
        input_template:

    Returns:
    -------
        None

    """
    input_timestamp = datetime.datetime(2023, 10, 30, 0, 0)

    result = _render_uca_data(input_uca_data, input_settings, input_template, input_timestamp)
    assert len(result) == 1


def test_generate_uca_data_from_CSV(input_settings, input_template):
    """
    Test to generate UCA data

    Args:
    ----
        input_uca_data:
        input_settings:
        input_template:

    Returns:
    -------
        None

    """
    test_data_file = str((Path(__file__).parent / "../data/test_data.csv").resolve())
    test_data = load_data_files(test_data_file, "CSV")
    uca_to_send = generate_uca(None, input_template, input_settings, test_data)
    assert len(uca_to_send) == 12
    for x, li in enumerate(uca_to_send):
        assert test_data[x]["unit_value"] == li["value"]
        assert test_data[x]["timestamp"] == li["timestamp"]
        assert test_data[x]["unit_id"] == li["id"]
