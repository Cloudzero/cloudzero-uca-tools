#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

from datetime import datetime
from typing import NamedTuple

from dateutil import parser


class TimeRange(NamedTuple):

    """
    TimeRange class
    """

    start: datetime
    end: datetime

    def __str__(self):
        """
        Return a string representation of TimeRange

        Returns
        -------
            str

        """
        return f"{self.start} - {self.end}"

    def serializable(self):
        """
        Serialize TimeRange

        Returns
        -------
            dict

        """
        return {k: v.isoformat() for k, v in self._asdict().items()}

    @staticmethod
    def load(x: dict):
        """
        Load TimeRange

        Args:
        ----
            x: dict

        Returns:
        -------
            TimeRange

        """
        return TimeRange(**{k: parser.isoparse(v) for k, v in x.items()})
