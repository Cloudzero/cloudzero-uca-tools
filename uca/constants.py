# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

from botocore.config import Config

DATE_FORMAT = '%Y-%m-%d'
TIME_FORMAT = f'{DATE_FORMAT}T%H:%M:%SZ'
SECONDS_PER_YEAR = 31536000
SECONDS_PER_WEEK = 604800
SECONDS_PER_DAY = 86400
SECONDS_PER_HOUR = 3600

MAX_BOTO3_SESSION_LENGTH = 900  # Time in seconds until boto3 sessions/clients should be refreshed

UCA_VERSION_1_2 = 'v1.2'
UCA_VERSION_1_3 = 'v1.3'
DEFAULT_UCA_VERSION = UCA_VERSION_1_2
SUPPORTED_UCA_VERSIONS = [UCA_VERSION_1_2, UCA_VERSION_1_3]
DEFAULT_UCA_GRANULARITY = 'HOURLY'

UCA_API_BATCH_SIZE = 3000


def common_boto3_client_config():
    """
    Common Boto3 Client Config

    General settings we should use for all Boto3 client connections.

    Things this client config does:
    1. Configure retry adaptive mode and set max attempts to 15

    Returns:
        Config (botocore.config)

    """
    config = Config(
        # region_name='us-east-1',
        retries=dict(
            max_attempts=15,
            mode='adaptive'
        )
    )
    return config
