#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import csv
import gzip
import os
import pathlib
import sys

import botocore
import simplejson as json

from uca.common.aws import get_s3_client, list_s3_bucket_contents, open_file_from_s3
from uca.common.cli import eprint
from uca.common.formatters import parse_url
from uca.constants import SUPPORTED_FILE_EXTENSIONS


def open_local_file(file_path: pathlib.PurePath):
    """
    Open a local file for reading

    Args:
    ----
        file_path:

    Returns:
    -------
        file object

    """
    if file_path.suffix == ".gz":  # poor man's GZip detection
        raw_file = gzip.open(file_path, mode="r", newline="", encoding="utf-8-sig")
    else:
        raw_file = open(file_path, newline="", encoding="utf-8-sig")
    return raw_file


def list_all_local_files_in_path(root_path: str) -> list:
    """
    Return a list of PurePath objects for all files in and below the provided root path

    Args:
    ----
        root_path (str):

    Returns:
    -------
        list

    """
    all_files = []
    for path, _subdirs, files in os.walk(root_path):
        for name in files:
            full_path = pathlib.PurePath(path, name)
            if full_path.suffix in SUPPORTED_FILE_EXTENSIONS:
                all_files.append(full_path)
    return all_files


def load_data_files(source: str, file_format: [str] = None) -> list:
    """
    Load data from files located locally or in S3

    Args:
    ----
        source (str):
        file_format (str, None): CSV, JSON, None (None means just plain ASCII or UTF-8 text)

    Returns:
    -------
        list:

    """
    if not file_format:
        file_format = "TEXT"

    if file_format not in ["TEXT", "JSON", "CSV"]:
        eprint(f"ERROR: {file_format} is unsupported, must be TEXT, JSON or CSV")
        sys.exit(1)

    loaded_records = []
    if source.lower().startswith("s3://"):
        print(f" - Reading {file_format} from S3")

        bucket, key = parse_url(source)
        client = get_s3_client()

        try:
            if source.lower().endswith("/"):  # load all files in bucket
                files = list(list_s3_bucket_contents(client, bucket, prefix=key))
                print(f" - Found {len(files)} files")
            else:
                files = [key]

            print("   --------------------------------------------------------------------------------------")
            for file in files:
                fp = open_file_from_s3(client, bucket, file["Key"])
                if file_format == "JSON":
                    records = fp.readlines()
                    loaded_records += [json.loads(x) for x in records]
                elif file_format.upper() == "CSV":
                    csv_data = csv.DictReader(fp)
                    records = list(csv_data)
                    loaded_records += records
                else:
                    records = fp.readlines()
                    loaded_records += records
                print(f"   > {file['Key']} ({len(records)} lines | {sys.getsizeof(records):,} bytes)")

        except botocore.exceptions.ClientError:
            eprint(f"\nERROR: Access denied, please ensure your AWS session has access to {source}")
            sys.exit(1)

    else:  # input is a local file or directory
        print(f" - Reading {file_format} from local files")
        if "file://" not in source:
            source = f"file://{os.path.expanduser(source)}"

        folder, file_name = parse_url(source)
        if not file_name:  # we have a folder
            files = list_all_local_files_in_path(folder)
        else:
            files = [pathlib.PurePath(folder, file_name)]

        for file in files:
            try:
                with open_local_file(file) as fp:
                    if file_format == "JSON":
                        records = fp.readlines()
                        loaded_records += [json.loads(x) for x in records]
                    elif file_format.upper() == "CSV":
                        csv_data = csv.DictReader(open(file, newline="", encoding="utf-8-sig"))
                        records = list(csv_data)
                        loaded_records += records
                    else:
                        records = fp.readlines()
                        loaded_records += records
                print(f"   > {file} ({len(records)} lines | {sys.getsizeof(records):,} bytes)")
            except Exception as error:
                eprint(f"Unable to read file {file}, error: {error}")
                sys.exit(-1)

    return loaded_records


def load_jsonl(file_path):
    """
    Load a JSONL file into a list of dictionaries

    Args:
    ----
        file_path:

    Returns:
    -------
        list[dict]

    """
    data = []
    with open(file_path) as file:
        for line in file:
            data.append(json.loads(line))
    return data


def write_to_file(uca_to_send: list[dict], output_file: str):
    """
    Write data to a file

    Args:
    ----
        uca_to_send:
        output_file:

    Returns:
    -------
        None

    """
    with open(os.path.expanduser(output_file), "w") as fp:
        for line in uca_to_send:
            try:
                fp.write(json.dumps(line) + "\n")
            except Exception as error:
                eprint(f"Unable to write data to file {output_file}, error: {error}")
                eprint(f"Data: {line}")
                sys.exit(-1)
