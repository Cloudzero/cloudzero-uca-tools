#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import gzip
import sys
from datetime import datetime
from io import BytesIO, TextIOWrapper
from typing import Optional

import boto3
import botocore

from uca.common.cli import eprint


def list_s3_bucket_contents(
    client,
    bucket_name,
    prefix="/",
    delimiter="/",
    cursor: Optional[str] = None,
    last_modified: Optional[datetime] = None,
):
    """
    List the contents of an S3 bucket

    Args:
    ----
        client:
        bucket_name:
        prefix:
        delimiter:
        cursor:
        last_modified:

    Returns:
    -------
        Generator

    """
    s3_paginator = client.get_paginator("list_objects_v2")
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    cursor = f"{prefix}{cursor}" if cursor else ""
    for page in s3_paginator.paginate(Bucket=bucket_name, Prefix=prefix, StartAfter=cursor):
        for content in page.get("Contents", ()):
            if last_modified:
                if content["LastModified"] > last_modified:
                    yield content
            else:
                yield content


def open_file_from_s3(client, bucket, key):
    """
    Open a file from S3

    Args:
    ----
        client:
        bucket:
        key:

    Returns:
    -------
        TextIOWrapper

    """
    response = client.get_object(Bucket=bucket, Key=key)
    if ".gz" in key:  # poor man's GZip detection
        raw_file = gzip.open(BytesIO(response["Body"].read()), mode="rt", encoding="utf-8")
    else:
        raw_file = TextIOWrapper(BytesIO(response["Body"].read()), encoding="utf-8")
    return raw_file


def get_s3_client():
    """
    Get an S3 client

    Returns
    -------
        boto3.client

    """
    try:
        client = boto3.client("sts")
        result = client.get_caller_identity()
        print(f" - AWS Authenticated: {result['Arn']}")
        client = boto3.client("s3")
    except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ClientError):
        eprint("\nERROR: AWS Credentials missing or expired, please check your AWS session and try again")
        sys.exit(1)
    return client
