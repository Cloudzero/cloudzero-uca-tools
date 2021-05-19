# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
from datetime import datetime
from decimal import Decimal
from enum import Enum

import simplejson as json


class JSONSanity(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, set):
            return list(o)
        if isinstance(o, Decimal):
            return str(o)
        if isinstance(o, Enum):
            return o.value
        if isinstance(o, datetime):
            return o.isoformat()
        if isinstance(o, float):
            return str(o)
        return super(JSONSanity, self).default(o)


def chunks(li, n):
    """
    Yield successive n-sized chunks from li.
    """
    for i in range(0, len(li), n):
        yield li[i:i + n]


def serialize_for_dynamodb(data):
    return json.loads(json.dumps(data, cls=JSONSanity))
