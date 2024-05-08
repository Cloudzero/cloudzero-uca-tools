#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com


import functools
import os
from datetime import datetime
from decimal import Decimal
from enum import Enum
from urllib.parse import urlparse

import simplejson as json

from uca.exceptions import MalformedUrl


class JSONSanity(json.JSONEncoder):

    """
    JSON encoder that handles Decimal, Enum, datetime, and sets
    """

    def default(self, o):
        """
        Perform sane serialization

        Args:
        ----
            o:

        Returns:
        -------
            object

        """
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
        return super().default(o)


def chunks(li, n):
    """
    Yield successive n-sized chunks from li.
    """
    for i in range(0, len(li), n):
        yield li[i : i + n]


def serialize_for_dynamodb(data):
    """
    Serialize data for DynamoDB

    Args:
    ----
        data:

    Returns:
    -------
        object

    """
    return json.loads(json.dumps(data, cls=JSONSanity))


def parse_url(url):
    """
    Parse an URL, returning a tuple containing the bucket name and key, supports s3 or file

    Args:
    ----
        url (string): URL, like s3://some_bucket/some_path/and/maybe/a.file

    Returns (tuple): bucket/root folder (some_location), file (some_path/and/maybe/a.file)

    >>> parse_url("s3://some_bucket/some_path/and/no/file/")
    ('some_bucket', 'some_path/and/no/file/')

    >>> parse_url("s3://some_bucket/some_path/and/maybe/a.file")
    ('some_bucket', 'some_path/and/maybe/a.file')

    >>> parse_url("s3://some_bucket/some_path//with/extra/but/valid/slashes//a.file")
    ('some_bucket', 'some_path//with/extra/but/valid/slashes//a.file')

    >>> parse_url("s3://some_bucket/")
    ('some_bucket', '')

    >>> parse_url("file://some_file.json")
    ('', 'some_file.json')

    >>> parse_url("file://some_folder/some_file.json")
    ('some_folder', 'some_file.json')

    >>> parse_url("file://some_folder/with_a_path/some_file.json")
    ('some_folder/with_a_path', 'some_file.json')

    >>> parse_url("file://some_folder/with_a_path_but_no_file/")
    ('some_folder/with_a_path_but_no_file', '')

    >>> parse_url("sdfsdfsdfsf")
    Traceback (most recent call last):
    ...
    uca.exceptions.MalformedUrl:  url 'sdfsdfsdfsf' is malformed or unsupported

    """
    parsed_url = urlparse(url)
    if str(parsed_url.scheme) == "s3":
        root = parsed_url.netloc
        file = parsed_url.path.lstrip("/")
    elif str(parsed_url.scheme) == "file":
        root, file = os.path.split(f"{parsed_url.netloc}{parsed_url.path}")
    else:
        raise MalformedUrl(f"{parsed_url.scheme} url '{url}' is malformed or unsupported")
    return root, file


def rgetattr(obj, attr, *args):
    """
    Recursively get an attribute from an object

    Args:
    ----
        obj:
        attr:
        *args:

    Returns:
    -------
        object

    """

    def _getattr(obj, attr):
        return getattr(obj, attr, *args)

    return functools.reduce(_getattr, [obj, *attr.split(".")])
