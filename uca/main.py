#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import os
import sys
from datetime import datetime, timedelta

import click
import simplejson as json

from uca.__version__ import __version__
from uca.common.cli import eprint, print_uca_sample
from uca.common.custom_types import TimeRange
from uca.common.files import load_data_files, write_to_file
from uca.common.standards import utc_datetime_from_anything
from uca.constants import FILE_FORMATS, DEFAULT_FILE_FORMAT
from uca.exceptions import InvalidDate
from uca.features.convert import convert
from uca.features.generate import generate_uca
from uca.features.transform import transform_data, load_transform_script
from uca.features.transmit import transmit


class RootConfiguration(object):
    def __init__(self, configuration=None, dry_run=False, api_key=False):
        if configuration:
            self.configuration_path = os.path.abspath(configuration)
            self.settings, self.template = self.load_settings()
        else:
            self.settings = {}
            self.template = {}
        self.output_path = None
        self.dry_run = dry_run
        self.api_key = api_key or self.settings.get("api_key")
        self.granularity = self.template.get("granularity")

        if self.dry_run:
            print(self.dry_run)
            self.dry_run = True
            self.destination = "nowhere (dry run only)"
        elif self.api_key:
            self.destination = "CloudZero API"

    def print(self):
        print(
            f" Configuration: {self.configuration_path}\n"
            f"       Dry Run: {self.dry_run}\n"
            f"       API Key: {self.api_key}\n"
            f"   Destination: {self.destination}"
        )

    def load_settings(self):
        try:
            with open(self.configuration_path, mode="r") as fp:
                configuration_file = json.load(fp)
                uca_settings = configuration_file["settings"]
                uca_template = configuration_file["template"]
        except Exception as error:
            eprint(
                f"Unable to read configuration file {self.configuration_path}, error: {error}"
            )
            sys.exit(-1)
        return uca_settings, uca_template


pass_root_configuration = click.make_pass_decorator(RootConfiguration)


def add_version(f):
    """
    Add the version of the tool to the help heading.
    """
    f.__doc__ += f" (v{__version__})"
    return f


@click.group(name="cloudzero-uca-tools")
@click.version_option(version=__version__)
@click.option(
    "--configuration", "-c", required=False, help="UCA configuration file (JSON)"
)
@click.option(
    "--dry-run",
    "-dry",
    is_flag=True,
    required=False,
    help="Perform a dry run, read and transform the data but do not send it to the API. "
    "Sample events will be output to the screen",
)
@click.option(
    "--api-key", "-k", required=False, envvar="CZ_API_KEY", help="API Key to use"
)
@click.pass_context
@add_version
def cli(ctx, configuration, dry_run, api_key):
    """CloudZero Unit Cost Analytics toolkit"""
    ctx.obj = RootConfiguration(
        configuration=configuration, dry_run=dry_run, api_key=api_key
    )


@cli.command("generate")
@click.option(
    "--start", "-s", required=False, help="start datetime <YYYY-MM-DD HH:MM:SS>"
)
@click.option("--end", "-e", required=False, help="End datetime <YYYY-MM-DD HH:MM:SS>")
@click.option(
    "--today", is_flag=True, required=False, help="Generate events for the current day"
)
@click.option("--input", "-i", required=True, help="Input UCA data (CSV)")
@click.option("--output", "-o", required=True, help="Output file")
@pass_root_configuration
def generate_uca_command(configuration, start, end, today, input, output):
    if not configuration.settings:
        eprint("Please specify a --configuration file")
        sys.exit()

    output = os.path.abspath(output)
    configuration.output_path = output
    configuration.destination = "File"

    if today:
        today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        range_requested = TimeRange(start=today, end=today + timedelta(days=1))
    elif all([start, end]):
        try:
            start_date = utc_datetime_from_anything(start)
        except InvalidDate as error:
            print(f"Invalid start date: {error}")
            sys.exit(-1)
        try:
            end_date = utc_datetime_from_anything(end)
        except InvalidDate as error:
            print(f"Invalid end date: {error}")
            sys.exit(-1)
        range_requested = TimeRange(start=start_date, end=end_date)
    else:
        range_requested = None

    try:
        generate_settings = configuration.settings["generate"]

        if not isinstance(generate_settings, dict):
            raise TypeError("generate_settings must be a dictionary")

        required_generate_keys = ["mode"]
        missing_keys = [
            key for key in required_generate_keys if key not in generate_settings
        ]
        if missing_keys:
            raise ValueError(
                f"Missing required key(s) in 'generate' config: {', '.join(missing_keys)}"
            )

        print("CloudZero UCA Data Generator")
        print("-" * 140)
        print(f"   Date Range : {range_requested or 'data driven'}")
        if "metric-name" not in configuration.template:
            print(f"  Granularity : {configuration.template['granularity']}")
        print(f"         Mode : {generate_settings['mode']}")
        if generate_settings["mode"] == "jitter":
            print(f"       Jitter : {generate_settings['jitter']}")
        elif generate_settings["mode"] == "allocation":
            print(f"   Allocation : {generate_settings['allocation']}")
            if generate_settings.get("jitter"):
                print(f"              : with Jitter {generate_settings['jitter']}")
        if generate_settings.get("precision"):
            print(f"    Precision : {generate_settings['precision']}")
        print(f"Configuration : {configuration.configuration_path}")
        print(f"   Input Data : {input}")
        print(f"  Output File : {configuration.output_path}")
        print("-" * 140)

    except KeyError as error:
        eprint(f"Missing configurations: {error}")
        sys.exit(-1)
    except TypeError:
        eprint("'Generate' configuration must be a dictionary.")
        sys.exit(-1)
    except ValueError as error:
        eprint(error)
        sys.exit(-1)

    try:
        uca_data = load_data_files(input, "CSV")
    except Exception as error:
        eprint(f"Unable to read input file {input}, error: {error}")
        sys.exit(-1)

    uca_to_send = generate_uca(
        range_requested, configuration.template, generate_settings, uca_data
    )
    if not uca_to_send:
        print(f" - Event Generation failed, {len(uca_to_send)} events created")
        sys.exit(-1)

    print(f" - Event Generation complete, {len(uca_to_send)} events created")

    print_uca_sample(uca_to_send)

    print(f"\n - Writing UCA data to {output}")
    write_to_file(uca_to_send, output)


@cli.command("transmit")
@click.option(
    "--data",
    "-d",
    required=True,
    help="Source JSON data, in text or gzip + text format, supports file:// or s3:// paths",
)
@click.option(
    "--output",
    "-o",
    required=False,
    help="Instead of transmitting the data to the CloudZero API, Save the output to a file.",
)
@click.option(
    "--transform",
    "-t",
    required=False,
    help="Optional transformation script using jq (https://stedolan.github.io/jq/). "
    "Used when the source data needs modification or cleanup. See README.md for usage instructions",
)
@pass_root_configuration
def transmit_uca_command(configuration, data, output, transform):
    if output:
        configuration.output_path = output
        configuration.destination = "File"

    if 'telemetry-stream' in configuration.template:
        stream_name = configuration.template['telemetry-stream']
        stream_type = 'allocation'

    elif 'metric-name' in configuration.template:
        stream_name = configuration.template['metric-name']
        stream_type = 'metric'

    else:
        print("Missing 'telemetry-stream' or 'metric-name' key in 'template' config:")
        sys.exit(-1)

    print(f"Transmitting UCA data from {data} to {configuration.destination}")
    print("-" * 140)

    records = load_data_files(data, file_format="JSON")
    transform_script = load_transform_script(transform)
    uca_to_send, transformed_records, filtered_records = transform_data(
        records, transform_script
    )

    transmit_type = "sum"
    if "transmit_type" in configuration.settings and configuration.settings["transmit_type"].lower() in ["sum", "update", "delete"]:
        transmit_type = configuration.settings["transmit_type"]

        if configuration.settings["transmit_type"] == "delete":
            for record in uca_to_send:
                try:
                    del record["value"]

                except KeyError:
                    pass

    print(
        f" - Processed {len(records)} records "
        f"| {transformed_records} Transformed | {filtered_records} Filtered"
    )
    print(f" - {len(records) - filtered_records} records ready for transmission")
    print_uca_sample(uca_to_send)
    transmit(
        stream_name.lower(),
        stream_type.lower(),
        transmit_type.lower(),
        uca_to_send,
        configuration.output_path,
        configuration.api_key,
        configuration.dry_run,
    )


@cli.command("convert")
@click.option(
    "--data",
    "-d",
    required=True,
    help="Source data, in text or gzip + text format, supports file:// or s3:// paths",
)
@click.option(
    "--output", "-o", required=True, help="Destination file for converted data"
)
@pass_root_configuration
def convert_uca_command(configuration, data, output):
    output = os.path.abspath(output)
    if not configuration.settings:
        eprint("Please specify a --configuration file")
        sys.exit()
    else:
        configuration.output_path = output
        configuration.destination = "File"

    data_format = configuration.settings["convert"]["format"]
    print(f"Converting {data_format} data into CloudZero UCA")
    print("-" * 140)
    print(f"       Format : {data_format}")
    print("-" * 140)

    file_format = FILE_FORMATS.get(data_format, DEFAULT_FILE_FORMAT)
    records = load_data_files(data, file_format)
    converted_data = convert(records, configuration)

    print(
        f" - Aggregated {len(records)} {data_format} records into {len(converted_data)} UCA records"
    )
    print_uca_sample(converted_data)

    print(f"\n - Writing UCA data to {output}")
    write_to_file(converted_data, output)


@cli.command("delete-stream")
@click.option(
    "--stream",
    "-s",
    required=True,
    help="Name of a CloudZero telemetry stream",
)
def delete_telemetry_stream(stream):
    print(stream)


if __name__ == "__main__":
    cli()
