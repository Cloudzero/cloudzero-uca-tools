#  Copyright (c) 2021-2024 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com
import os

from uca.common.cli import print_uca_sample
from uca.common.files import load_jsonl


def test_print_uca_sample():
    """
    Tests print_uca_sample function for selected number of samples

    Returns
    -------
    None

    """
    # load sample uca data
    uca_sample_data_path = os.path.join(os.path.dirname(__file__), "../data/sample_uca_data.jsonl")
    uca_data = load_jsonl(uca_sample_data_path)

    print("Running test\n\n")
    result = print_uca_sample(uca_data, 2)
    assert len(result) == 2

    result = print_uca_sample(uca_data, 4)
    assert len(result) == 4

    result = print_uca_sample(uca_data, 7)
    assert len(result) == 7

    result = print_uca_sample(uca_data, 20)
    assert len(result) == 16

    result = print_uca_sample(uca_data, 1)
    assert len(result) == 1

    result = print_uca_sample(uca_data, 0)
    assert len(result) == 0

    result = print_uca_sample([], 0)
    assert len(result) == 0
