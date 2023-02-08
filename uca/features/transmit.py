#  Copyright (c) 2021-2023 CloudZero, Inc. or its affiliates. All Rights Reserved.
#  SPDX-License-Identifier: Apache-2.0
#  Direct all questions to support@cloudzero.com

import sys

from uca.common.files import write_to_file
from uca.interfaces.uca_api import send_uca_events


def transmit(uca_to_send, output_file, api_key, dry_run):
    # order maters here, we want dry run to come first, if not that, output to file, if not that api key
    if dry_run:
        print('\nDry run, exiting')
        sys.exit()
    elif output_file:
        write_to_file(uca_to_send, output_file)
        print(f'\nWrote results to {output_file}')
    elif api_key:
        print('\nSending to API')
        send_uca_events(api_key, uca_to_send)
    else:
        print('\nFinished, nothing to do')


