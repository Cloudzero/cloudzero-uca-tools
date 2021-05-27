#!/usr/bin/env python3
# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import csv
import os
import random
import sys
from datetime import datetime, timedelta

import boto3
import botocore
import click
import simplejson as json

from uca.common.aws import list_s3_bucket_contents, read_file_from_s3
from uca.common.cli import eprint
from uca.common.custom_types import TimeRange
from uca.common.formatters import parse_url
from uca.common.standards import utc_datetime_from_anything
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
              required=False,
              help="start datetime <YYYY-MM-DD HH:MM:SS>")
@click.option("--end", "-e",
              required=False,
              help="End datetime <YYYY-MM-DD HH:MM:SS>")
@click.option("--today",
              is_flag=True,
              required=False,
              help="Generate events for the current day")
@click.option("--configuration", "-c",
              required=True,
              help="UCA configuration file (JSON)")
@click.option("--data", "-d",
              required=True,
              help="Input UCA data (CSV)")
@click.option("--output", "-o",
              required=False,
              help="Instead of sending events to the API, append the events to an output file")
@click.option("--api-key", "-k",
              required=False,
              help="API Key to use")
@click.option("--dry-run", "-dry",
              is_flag=True,
              required=False,
              help="Perform a dry run, read and transform the data but do not send it to the API")
def generate_uca_command(start, end, today, configuration, data, output, api_key, dry_run):
    if today:
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        range_requested = TimeRange(start=today, end=today + timedelta(days=1))
    elif all([start, end]):
        start_date = utc_datetime_from_anything(start)
        end_date = utc_datetime_from_anything(end)
        range_requested = TimeRange(start=start_date, end=end_date)
    else:
        eprint("Please specify either a start and end range or use the --today option to generate events for today")
        sys.exit()

    configuration = os.path.abspath(configuration)
    data = os.path.abspath(data)

    try:
        with open(configuration, mode='r') as fp:
            configuration_file = json.load(fp)
            uca_settings = configuration_file['settings']
            uca_template = configuration_file['template']

        data_file = csv.DictReader(open(data, mode='r', newline='', encoding="utf-8-sig"))  # keep fp open
    except Exception as error:
        eprint(f"Unable to read configuration or data, error: {error}")
        sys.exit(-1)

    api_key = api_key or uca_settings.get('api_key') or None

    print("CloudZero UCA Data Generator")
    print("-----------------------------------------------------------------------------------------")
    print(f"   Date Range : {range_requested}")
    print(f"  Granularity : {uca_template['granularity']}")
    print(f"         Mode : {uca_settings['mode']}")
    if uca_settings['mode'] == "jitter":
        print(f"       Jitter : {uca_settings['jitter']}")
    elif uca_settings['mode'] == "allocation":
        print(f"   Allocation : {uca_settings['allocation']}")
    print(f"Configuration : {configuration}")
    print(f"         Data : {data}")
    print(f"      API Key : {api_key and api_key[:5] + '...snip' or '(no key provided)'}")
    print("-----------------------------------------------------------------------------------------")

    uca_events = generate_uca(range_requested, uca_template, uca_settings, data_file)
    print(f"Event Generation complete, {len(uca_events)} events created\n")
    sample_count = min(5, len(uca_events))
    print(f"Random sample of {sample_count} events generated:")
    for x in sorted(random.sample(range(len(uca_events)), sample_count)):
        print(f"{x:7} : {uca_events[x]}")
    print("\n")

    if dry_run:
        print(' - Dry run, exiting')
        sys.exit()
    elif api_key:
        print(' - Sending to API')
        send_uca_events(api_key, uca_events)
    elif output:
        with open(os.path.expanduser(output), 'a') as output_file:
            for line in uca_events:
                output_file.write(json.dumps(line) + '\n')


@cli.command("transmit")
@click.option("--source", "-s",
              required=True,
              help="Source data, in text or gzip + text format, supports file:// or s3:// paths")
@click.option("--transform", "-t",
              required=False,
              help="Optional transformation script using jq (https://stedolan.github.io/jq/). Used when the source data needs modification or cleanup. See README.md for supported formats and usage instructions")
@click.option("--api-key", "-k",
              required=False,
              help="API Key to use")
@click.option("--output", "-o",
              required=False,
              help="Instead of sending events to the API, append the events to an output file")
@click.option("--configuration", "-c",
              required=False,
              help="UCA configuration file (JSON)")
@click.option("--dry-run", "-dry",
              is_flag=True,
              required=False,
              help="Perform a dry run, read and transform the data but do not send it to the API")
def transmit_uca_command(source, transform, api_key, output, configuration, dry_run):
    print(f"Transmitting data from {source} to CloudZero")
    print("-----------------------------------------------------------------------------------------")

    if configuration:
        configuration = os.path.abspath(configuration)
        try:
            with open(configuration, mode='r') as fp:
                configuration_file = json.load(fp)
                uca_settings = configuration_file['settings']
        except Exception as error:
            eprint(f"Unable to read configuration, error: {error}")
            sys.exit(-1)
    else:
        uca_settings = {'settings': {'api_key': api_key}}

    api_key = uca_settings.get('api_key') or None

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

    uca_to_send = []
    if source.lower().startswith('s3://'):
        print(" - Reading from S3")
        bucket, key = parse_url(source)

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
                    uca_data, good_records, bad_records = transform_file(file_data, transform_script)
                    print(
                        f" - s3://{bucket}/{file['Key']} | {good_records} events ({bad_records} bad) | {sys.getsizeof(file_data):,} bytes")
                    uca_to_send += uca_data

            else:
                print(f" - s3://{bucket}/{key}\n")
                print("   --------------------------------------------------------------------------------------")
                file_data = read_file_from_s3(client, bucket, key).readlines()
                uca_to_send, good_records, bad_records = transform_file(file_data, transform_script)
                print(f" - {good_records} events ({bad_records} bad) | {sys.getsizeof(file_data):,} bytes")

        except botocore.exceptions.ClientError:
            eprint(f"\nERROR: Access denied, please ensure your AWS session has access to {source}")
            sys.exit(1)

    elif source.lower().startswith('file://'):
        print(f" - Reading files from {source}")
        folder, file = parse_url(source)
        source_path = os.path.abspath(f"{folder}/{file}")
        try:
            with open(source_path, mode='r') as fp:
                file_data = fp.readlines()
        except Exception as error:
            eprint(f"Unable to read configuration, error: {error}")
            sys.exit(-1)

        uca_to_send, good_records, bad_records = transform_file(file_data, transform_script)
        print(f" - {good_records} events ({bad_records} bad) | {sys.getsizeof(file_data):,} bytes")

    else:
        print("Source path should start with either file:// or s3://")
        sys.exit()

    sample_count = min(5, len(uca_to_send))
    print(f"\n - Random sample of {sample_count} events processed:")
    for x in sorted(random.sample(range(len(uca_to_send)), sample_count)):
        print(f"{x:5} : {uca_to_send[x]}")

    if dry_run:
        print(' - Dry run, exiting')
        sys.exit()
    elif api_key:
        print(' - Sending to API')
        send_uca_events(api_key, uca_to_send)
    elif output:
        with open(os.path.expanduser(output), 'a') as output_file:
            for line in uca_to_send:
                output_file.write(json.dumps(line) + '\n')
    else:
        print(' - Finished, nothing to do')


if __name__ == "__main__":
    cli()
