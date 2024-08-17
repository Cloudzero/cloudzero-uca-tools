#  Copyright (c) 2024 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com
from pathlib import Path

from uca.common.files import load_data_files


def test_load_data_files():
    """
    Test to load data files
    """
    test_data_file = str((Path(__file__).parent / "../data/test_data.csv").resolve())
    data_files = load_data_files(test_data_file, "TEXT")
    assert len(data_files) == 13

    data_files = load_data_files(test_data_file, "CSV")
    assert len(data_files) == 12
