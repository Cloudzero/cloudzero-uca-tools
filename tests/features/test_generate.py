#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import datetime

from uca.features.generate import _render_uca_data


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
