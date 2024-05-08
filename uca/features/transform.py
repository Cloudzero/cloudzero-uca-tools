#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import os
import sys

import jq
import simplejson as json

from uca.common.cli import eprint


def compile_transform(jq_script):
    """
    Compile a jq script

    Args:
    ----
        jq_script:

    Returns:
    -------
        object

    """
    return jq.compile(jq_script)


def apply_transform(jq_program, input_data):
    """
    Apply a jq program to input data

    Args:
    ----
        jq_program:
        input_data:

    Returns:
    -------
        list

    """
    if jq_program:
        return jq_program.input(input_data).all()
    else:
        return input_data


def transform_data(input_data, transform_script):
    """
    Transform data using a jq script

    Args:
    ----
        input_data:
        transform_script:

    Returns:
    -------
        tuple(list, int, int)

    """
    data_to_send = []
    transformed_count = 0
    filtered_count = 0

    if not transform_script:
        return input_data, transformed_count, filtered_count

    jq_program = compile_transform(transform_script)
    for line in input_data:
        transformed_line = apply_transform(jq_program, json.loads(line))
        if transformed_line:
            data_to_send.append(transformed_line)
            transformed_count += 1
        else:
            filtered_count += 1
    return data_to_send, transformed_count, filtered_count


def load_transform_script(transform):
    """
    Load a transform script

    Args:
    ----
        transform:

    Returns:
    -------
        str

    """
    transform_script = None
    if transform:
        transform_file_path = os.path.expanduser(transform)
        if os.path.isfile(transform_file_path):
            print(f" - Applying {transform} transform script")
            with open(transform_file_path) as file:
                transform_script = file.read()
        else:
            eprint(f"Could not read {transform_file_path}, please check file and try again")
            sys.exit(1)
    return transform_script
