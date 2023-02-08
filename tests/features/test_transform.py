#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

from uca.features.transform import apply_transform, compile_transform


def test_apply_transform():
    input = {
        "uca": "v1.3",
        "timestamp": "2021-05-16 21:00:00+0000",
        "granularity": "HOURLY",
        "cost-context": "fred",
        "id": "sandy",
        "target": {},
        "telemetry-stream": "api-requests-per-second",
        "value": "234",
        "metadata": {
            "environment": "production"
        }
    }
    expected_output = {
        'cost-context': 'cost-per-title',
        'granularity': 'HOURLY',
        'id': 'sandy',
        'target': {
            'feature': ['fred'],
            'tag:environment': ['production']
        },
        'telemetry-stream': 'api-requests-per-second',
        'timestamp': '2021-05-16 21:00:00+0000',
        'value': '234'
    }

    jq = """select(.id != "")
    | .target = {"tag:environment": [.metadata.environment], "feature": [.["cost-context"]] }
    | .["cost-context"] = "cost-per-title"
    | del(.metadata, .uca)"""

    jq_program = compile_transform(jq)
    result = apply_transform(jq_program, input)
    assert result[0] == expected_output
