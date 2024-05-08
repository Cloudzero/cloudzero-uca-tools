#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import random
import sys

from colored import attr, fg
from tabulate import tabulate


def eprint(*args, **kwargs):
    """
    Print to stderr

    Args:
    ----
        *args:
        **kwargs:

    Returns:
    -------
        None

    """
    print(*args, file=sys.stderr, **kwargs)


def get_input(question, default=None):
    """
    Get input from the user

    Args:
    ----
        question:
        default:

    Returns:
    -------
        str

    """
    if default:
        question = f"{question} [{default}]: "
    else:
        question += ": "

    question = "{}{}{}".format(fg("light_green"), question, attr("reset"))

    result = input(question).strip()
    if result:
        return result
    else:
        return default


def confirm(prompt=None, resp=False):
    """
    Prompts for yes or no response from the user. Returns True for yes and False for no.

    'resp' should be set to the default value assumed by the caller when
    user simply types ENTER.

    >> confirm(prompt='Create Directory?', resp=True)
    Create Directory? [y]|n:
    True
    >> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y:
    False
    >> confirm(prompt='Create Directory?', resp=False)
    Create Directory? [n]|y: y
    True

    :param prompt:
    :param resp:
    """
    if prompt is None:
        prompt = "Confirm"

    if resp:
        prompt = "{} [{}]|{} ".format(prompt, "y", "n")
    else:
        prompt = "{} [{}]|{} ".format(prompt, "n", "y")

    while True:
        ans = get_input(prompt)
        if not ans:
            return resp
        if ans not in ["y", "Y", "n", "N"]:
            print("please enter y or n.")
            continue
        if ans in ("y", "Y"):
            return True
        if ans in ("n", "N"):
            return False


def print_uca_sample(uca_to_send, record_count=5):
    """
    Print a sample of UCA records post-processing

    Args:
    ----
        uca_to_send:
        record_count:

    Returns:
    -------
        list

    """
    if record_count == 0:
        return []

    if len(uca_to_send) == 0:
        eprint(" - No UCA records to sample.")
        return []

    sample_count = max(min(record_count, len(uca_to_send)), 1)
    sample_indexes = set(random.sample(range(len(uca_to_send)), sample_count))
    print(uca_to_send)
    sample_events = [uca_to_send[i] for i in sample_indexes]

    print(" - Sample of UCA records post-processing:")
    print(tabulate(enumerate(sample_events), headers=["#", "Record"], tablefmt="simple", maxcolwidths=[None, 240]))
    return sample_events
