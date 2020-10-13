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

import pytest


def test_get_symbiflow_arch_defs_tarball():
    from stpm import get_latest_artifact_url
    import requests
    import filetype

    url = get_latest_artifact_url('symbiflow-arch-defs', 'install')

    response = requests.get(url)
    ext = filetype.guess_extension(response.content)

    assert 'xz' is ext
