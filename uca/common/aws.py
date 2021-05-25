# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import gzip
from datetime import datetime
from io import BytesIO, TextIOWrapper


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
