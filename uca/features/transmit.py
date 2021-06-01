# Copyright (c) 2021 CloudZero, Inc. All rights reserved.
# Licensed under the BSD License. See LICENSE file in the project root for full license information.
# Direct all questions to support@cloudzero.com

import os
import sys

from uca.interfaces.uca_api import send_uca_events


def transmit(uca_to_send, output_file, api_key, dry_run):
    if dry_run:
        print('\nDry run, exiting')
        sys.exit()
    elif api_key:
        print('\nSending to API')
        send_uca_events(api_key, uca_to_send)
    elif output_file:
        with open(os.path.expanduser(output_file), 'w') as fp:
            for line in uca_to_send:
                fp.write(line.strip() + '\n')
        print(f'\nWrote results to {output_file}')
    else:
        print('\nFinished, nothing to do')
