#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (C) 2020  The SymbiFlow Authors.
#
# Use of this source code is governed by a ISC-style
# license that can be found in the LICENSE file or at
# https://opensource.org/licenses/ISC
#
# SPDX-License-Identifier:	ISC

import json
import requests


# For now we use only `symbiflow-arch-defs` and download tarballs
def get_latest_artifact_url(project='symbiflow-arch-defs', build_name='install'):
    base_url = f'https://www.googleapis.com/storage/v1/b/{project}/o'
    prefix = f'artifacts/prod/foss-fpga-tools/{project}/continuous/{build_name}/'
    params = {'prefix':prefix}
    urls_of_integers = {}

    to_strip = f'{project}/{prefix}'

    while True:
        r = requests.get(
                base_url,
                params=params,
                headers={"Content-Type": "application/json"},
                )
        r.raise_for_status()

        try:
            items = r.json()['items']
        except KeyError:
            return ''

        for obj in items:
            obj_int = int(obj['id'].replace(to_strip, '').split('/')[0])
            urls_of_integers[obj_int] = obj['mediaLink']

        try:
            params['pageToken'] = r.json()['nextPageToken']
        except KeyError:
            break

    try:
        max_int = max(urls_of_integers.keys())
    except ValueError:
        return ''

    return urls_of_integers[max_int]
