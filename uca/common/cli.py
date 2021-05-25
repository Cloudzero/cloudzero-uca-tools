# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com
import sys

from colored import fg, attr


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


def get_input(question, default=None):
    if default:
        question = "{} [{}]: ".format(question, default)
    else:
        question += ': '

    question = "{}{}{}".format(fg('light_green'), question, attr('reset'))

    result = input(question).strip()
    if result:
        return result
    else:
        return default


def confirm(prompt=None, resp=False):
    """
    prompts for yes or no response from the user. Returns True for yes and
    False for no.

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
        prompt = 'Confirm'

    if resp:
        prompt = '{0} [{1}]|{2} '.format(prompt, 'y', 'n')
    else:
        prompt = '{0} [{1}]|{2} '.format(prompt, 'n', 'y')

    while True:
        ans = get_input(prompt)
        if not ans:
            return resp
        if ans not in ['y', 'Y', 'n', 'N']:
            print('please enter y or n.')
            continue
        if ans == 'y' or ans == 'Y':
            return True
        if ans == 'n' or ans == 'N':
            return False
