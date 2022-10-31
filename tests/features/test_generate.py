# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

import datetime

from uca.features.generate import _render_uca_data


def test_filter_nil_unit_values_exact_mode():
    input_uca_data = [{'unit_id': 'Sunbank', 'unit_value': '0'},
                      {'unit_id': 'SoftwareCorp', 'unit_value': '0'},
                      {'unit_id': 'Parts, Inc.', 'unit_value': '0'},
                      {'unit_id': 'Transport Co.', 'unit_value': '0'},
                      {'unit_id': 'WeShipit, Inc.', 'unit_value': '0'},
                      {'unit_id': 'CapitalTwo', 'unit_value': '0'},
                      {'unit_id': 'Bank of Sokovia', 'unit_value': '0'},
                      {'unit_id': 'Makers', 'unit_value': '0'},
                      {'unit_id': 'StateEx', 'unit_value': '0'},
                      {'unit_id': 'Flitter', 'unit_value': '0'},
                      {'unit_id': 'Pets2you', 'unit_value': '0'},
                      {'unit_id': 'Hooli', 'unit_value': '0'},
                      {'unit_id': 'Massive Dynamic', 'unit_value': '1000'}]

    input_settings = {'allocation': '', 'jitter': '', 'mode': 'exact'}

    input_template = {'cost-context': 'Cost-Per-Fake-Customer',
                      'granularity': 'DAILY',
                      'id': '$unit_id',
                      'target': {},
                      'telemetry-stream': 'test-data',
                                          'timestamp': '$timestamp',
                                          'value': '$unit_value'}

    input_timestamp = datetime.datetime(2022, 10, 30, 0, 0)

    result = _render_uca_data(input_uca_data, input_settings, input_template, input_timestamp)
    assert len(result) == 1


def test_filter_nil_unit_values_random_mode():
    input_uca_data = [{'unit_id': 'Sunbank', 'unit_value': '0'},
                      {'unit_id': 'SoftwareCorp', 'unit_value': '0'},
                      {'unit_id': 'Parts, Inc.', 'unit_value': '0'},
                      {'unit_id': 'Transport Co.', 'unit_value': '0'},
                      {'unit_id': 'WeShipit, Inc.', 'unit_value': '0'},
                      {'unit_id': 'CapitalTwo', 'unit_value': '0'},
                      {'unit_id': 'Bank of Sokovia', 'unit_value': '0'},
                      {'unit_id': 'Makers', 'unit_value': '0'},
                      {'unit_id': 'StateEx', 'unit_value': '0'},
                      {'unit_id': 'Flitter', 'unit_value': '0'},
                      {'unit_id': 'Pets2you', 'unit_value': '0'},
                      {'unit_id': 'Hooli', 'unit_value': '0'},
                      {'unit_id': 'Massive Dynamic', 'unit_value': '1000'}]

    input_settings = {'allocation': '', 'jitter': '', 'mode': 'random'}

    input_template = {'cost-context': 'Cost-Per-Fake-Customer',
                      'granularity': 'DAILY',
                      'id': '$unit_id',
                      'target': {},
                      'telemetry-stream': 'test-data',
                                          'timestamp': '$timestamp',
                                          'value': '$unit_value'}

    input_timestamp = datetime.datetime(2022, 10, 30, 0, 0)

    result = _render_uca_data(input_uca_data, input_settings, input_template, input_timestamp)
    assert len(result) == 1
