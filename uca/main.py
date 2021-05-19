#!/usr/bin/env python3
# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import csv
import os

import click

from uca.common.standards import utc_datetime_from_anything
from uca.common.types import TimeRange
from uca.features.generate import generate_uca


@click.group()
@click.version_option(version="0.0.1")
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


if __name__ == "__main__":
    cli()
