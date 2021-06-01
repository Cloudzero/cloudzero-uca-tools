# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import gzip
import os
import pathlib
import sys

import botocore

from uca.common.aws import list_s3_bucket_contents, open_file_from_s3, get_s3_client
from uca.common.cli import eprint
from uca.common.formatters import parse_url
from uca.constants import SUPPORTED_FILE_EXTENSIONS


def open_local_file(file_path: pathlib.PurePath):
    if file_path.suffix == ".gz":  # poor man's GZip detection
        raw_file = gzip.open(file_path, mode='rt', encoding='utf-8')
    else:
        raw_file = open(file_path, mode='rt', encoding='utf-8')
    return raw_file


def list_all_local_files_in_path(root_path: str) -> list:
    """
    Returns a list of PurePath objects for all files in and below the provided root path

    Args:
        root_path (str):

    Returns:
        list

    """
    all_files = []
    for path, subdirs, files in os.walk(root_path):
        for name in files:
            full_path = pathlib.PurePath(path, name)
            if full_path.suffix in SUPPORTED_FILE_EXTENSIONS:
                all_files.append(full_path)
    return all_files


def load_files(source):
    """
        Loads data from files located locally or in S3

    Args:
        source:

    Returns:

    """
    print(f" - Reading from {source}")
    loaded_records = []
    if source.lower().startswith('s3://'):
        bucket, key = parse_url(source)
        client = get_s3_client()

        try:
            if source.lower().endswith('/'):  # load all files in bucket
                files = list(list_s3_bucket_contents(client, bucket, prefix=key))
                print(f" - Found {len(files)} files")
            else:
                files = [key]

            print("   --------------------------------------------------------------------------------------")
            for file in files:
                records = open_file_from_s3(client, bucket, file['Key']).readlines()
                # yield records
                loaded_records += records
                print(f"   > {file['Key']} ({len(records)} lines | {sys.getsizeof(records):,} bytes)")

        except botocore.exceptions.ClientError:
            eprint(f"\nERROR: Access denied, please ensure your AWS session has access to {source}")
            sys.exit(1)

    elif source.lower().startswith('file://'):
        folder, file_name = parse_url(source)
        if not file_name:  # read all files in path
            files = list_all_local_files_in_path(folder)
        else:
            files = [pathlib.PurePath(folder, file_name)]

        for file in files:
            try:
                with open_local_file(file) as fp:
                    records = fp.readlines()
                    # yield records
                    loaded_records += records
                    print(f"   > {file} ({len(records)} lines | {sys.getsizeof(records):,} bytes)")
            except Exception as error:
                eprint(f"Unable to read file {file}, error: {error}")
                sys.exit(-1)
    else:
        print("Source path should start with either file:// or s3://")
        sys.exit()

    return loaded_records
