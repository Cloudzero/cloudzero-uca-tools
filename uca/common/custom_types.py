# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
from datetime import datetime
from typing import NamedTuple

from dateutil import parser


class TimeRange(NamedTuple):
    start: datetime
    end: datetime

    def __str__(self):
        return f'{self.start} - {self.end}'

    def serializable(self):
        return {k: v.isoformat() for k, v in self._asdict().items()}

    @staticmethod
    def load(x: dict):
        return TimeRange(**{k: parser.isoparse(v) for k, v in x.items()})
