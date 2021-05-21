# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import gzip
from datetime import datetime
from io import BytesIO, TextIOWrapper
from urllib.parse import urlparse


def list_s3_bucket_contents(client, bucket_name, prefix='/', delimiter='/', cursor=None,
                            last_modified: datetime = None):
    s3_paginator = client.get_paginator('list_objects_v2')
    prefix = prefix[1:] if prefix.startswith(delimiter) else prefix
    cursor = f"{prefix}{cursor}" if cursor else ''
    for page in s3_paginator.paginate(Bucket=bucket_name, Prefix=prefix, StartAfter=cursor):
        for content in page.get('Contents', ()):
            if last_modified:
                if content['LastModified'] > last_modified:
                    yield content
            else:
                yield content


def read_file_from_s3(client, bucket, key):
    response = client.get_object(Bucket=bucket, Key=key)
    if ".gz" in key:  # poor man's GZip detection
        raw_file = gzip.open(BytesIO(response['Body'].read()), mode='rt', encoding='utf-8')
    else:
        raw_file = TextIOWrapper(BytesIO(response['Body'].read()), encoding='utf-8')
    return raw_file


def parse_s3_url(s3_url):
    """
    Parse an S3 URL, returning a tuple containing the bucket name and key

    Args:
        s3_url (string): s3 URL, like s3://some_bucket/some_path/and/maybe/a.file

    Returns (tuple): bucket name (some_bucket), key (some_path/and/maybe/a.file)

    >>> parse_s3_url("s3://some_bucket/some_path/and/no/file/")
    ('some_bucket', 'some_path/and/no/file/')

    >>> parse_s3_url("s3://some_bucket/some_path/and/maybe/a.file")
    ('some_bucket', 'some_path/and/maybe/a.file')

    >>> parse_s3_url("s3://some_bucket/some_path//with/extra/but/valid/slashes//a.file")
    ('some_bucket', 'some_path//with/extra/but/valid/slashes//a.file')

    >>> parse_s3_url("s3://some_bucket/")
    ('some_bucket', '')

    >>> parse_s3_url("sdfsdfsdfsf")
    Traceback (most recent call last):
    ...
    aws.MalformedS3Url: S3 url 'sdfsdfsdfsf' is malformed

    """
    parsed_config_location = urlparse(s3_url)
    if parsed_config_location.scheme == 's3':
        bucket = parsed_config_location.netloc
        key = parsed_config_location.path.lstrip('/')
    else:
        raise MalformedS3Url(f"S3 url '{s3_url}' is malformed")
    return bucket, key


class MalformedS3Url(Exception):
    """Thrown when we have a malformed S3 URL"""
    pass
