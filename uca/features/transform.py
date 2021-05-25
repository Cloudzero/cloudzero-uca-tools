# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

import jq
import simplejson as json


def compile_transform(jq_script):
    return jq.compile(jq_script)


def apply_transform(jq_program, input_data):
    if jq_program:
        return jq_program.input(input_data).all()
    else:
        return input_data


def transform_file(file, transform_script):
    uca_data_to_send = []
    good_records = 0
    bad_records = 0
    jq_program = transform_script and compile_transform(transform_script) or None
    for line in file:
        data = apply_transform(jq_program, json.loads(line))
        if data:
            uca_data_to_send.append(data)
            good_records += 1
        else:
            bad_records += 1
    return uca_data_to_send, good_records, bad_records
