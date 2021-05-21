#!/usr/bin/env python3
# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import csv
import os
import sys

import boto3
import botocore
import click

from uca.common.aws import list_s3_bucket_contents, parse_s3_url, read_file_from_s3
from uca.common.cli import eprint
from uca.common.standards import utc_datetime_from_anything
from uca.common.types import TimeRange
from uca.features.generate import generate_uca
from uca.features.transform import transform_file
from uca.interfaces.uca_api import send_uca_events


@click.group()
@click.version_option(version="0.0.2")
def cli():
    """UCA Tool
    """
    pass


@cli.command("generate")
@click.option("--start", "-s",
              required=True,
              help="start datetime")
@click.option("--end", "-e",
              required=True,
              help="End datetime")
@click.option("--template", "-t",
              required=True,
              help="UCA JSON Template")
@click.option("--data", "-d",
              required=True,
              help="Input UCA data")
@click.option("--granularity", "-g",
              required=True,
              help="DAILY or HOURLY")
@click.option("--api-key", "-k",
              required=True,
              help="API Key to use")
def generate_uca_command(start, end, template, data, granularity, api_key):
    start_date = utc_datetime_from_anything(start)
    end_date = utc_datetime_from_anything(end)
    range_requested = TimeRange(start=start_date, end=end_date)

    template = os.path.abspath(template)
    data = os.path.abspath(data)

    print(f"Generating UCA Data to send to API")
    print("-----------------------------------------------------------------------------------------")
    print(f" Date Range : {range_requested}")
    print(f"   Template : {template}")
    print(f"       Data : {data}")
    print(f"Granularity : {granularity}")
    print(f"    API Key : {api_key[:5]}...")
    print("-----------------------------------------------------------------------------------------")

    template_file = open(template, mode='r').read().strip()
    data_file = csv.DictReader(open(data, mode='r', newline=''))
    result = generate_uca(range_requested, template_file, data_file, granularity, api_key)
    print(result)


@cli.command("transmit")
@click.option("--source", "-s",
              required=True,
              help="Source data, in text or gzip + text format, supports file:// or s3:// paths")
@click.option("--transform", "-t",
              required=False,
              help="Optional transformation script using jq (https://stedolan.github.io/jq/). Used when the source data needs modification or cleanup. See README.md for supported formats and usage instructions")
@click.option("--api-key", "-k",
              required=True,
              help="API Key to use")
@click.option("--dry-run", "-dry",
              is_flag=True,
              required=False,
              help="Perform a dry run, read and transform the data but do not send it to the API")
def transmit_uca_command(source, transform, api_key, dry_run):
    print(f"Transmitting data from {source} to CloudZero")
    print("-----------------------------------------------------------------------------------------")

    transform_script = None
    if transform:
        transform_file_path = os.path.expanduser(transform)
        if os.path.isfile(transform_file_path):
            print(f"Applying {transform} transform script")
            with open(transform_file_path, 'r') as file:
                transform_script = file.read()
        else:
            eprint(f"Could not read {transform_file_path}, please check file and try again")
            sys.exit(1)

    if source.lower().startswith('s3://'):
        print(" - Reading from S3")
        bucket, key = parse_s3_url(source)

        try:
            client = boto3.client('sts')
            result = client.get_caller_identity()
            print(f" - Authenticated: {result['Arn']}")
        except (botocore.exceptions.NoCredentialsError, botocore.exceptions.ClientError):
            eprint("\nERROR: AWS Credentials missing or expired, please check your AWS session and try again")
            sys.exit(1)

        try:
            client = boto3.client('s3')
            if source.lower().endswith('/'):
                result = list_s3_bucket_contents(client, bucket, prefix=key)
                files = list(result)
                print(f" - Found {len(files)} files")
                print("   --------------------------------------------------------------------------------------")
                for file in files:
                    file_data = read_file_from_s3(client, bucket, file['Key']).readlines()
                    uca_to_send, good_records, bad_records = transform_file(file_data, transform_script)
                    print(f" - s3://{bucket}/{file['Key']} | {good_records} events ({bad_records} bad) | {sys.getsizeof(file_data):,} bytes")
                    if not dry_run:
                        print('   Sending to API')
                        send_uca_events(api_key, uca_to_send)
                    else:
                        print('   Dry run, skipping send')
            else:
                print(f" - s3://{bucket}/{key}\n")
                print("   --------------------------------------------------------------------------------------")
                file_data = read_file_from_s3(client, bucket, key).readlines()
                uca_to_send = transform_file(file_data, transform_script)
                if not dry_run:
                    print('   Sending to API')
                    send_uca_events(api_key, uca_to_send)
                else:
                    print('   Dry run, skipping send')

        except botocore.exceptions.ClientError:
            eprint(f"\nERROR: Access denied, please ensure your AWS session has access to {source}")
            sys.exit(1)

    elif source.lower().starswith('file://'):
        print(" - Reading files from local path")
    else:
        print("Source path should start with either file:// or s3://")
        sys.exit()


if __name__ == "__main__":
    cli()
