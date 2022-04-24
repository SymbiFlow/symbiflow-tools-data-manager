#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright 2020-2022 F4PGA Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0

import pytest
import argparse

parser = argparse.ArgumentParser(description="Retrieves the latest artifacts of SymbiFlow-related CIs.")


def test_get_symbiflow_arch_defs_tarball():
    from stdm import get_latest_artifact_url
    import requests
    import filetype

    urls, build_number = get_latest_artifact_url("symbiflow-arch-defs", "install")

    url = urls[0]["url"]
    response = requests.get(url)
    ext = filetype.guess_extension(response.content)

    assert "xz" is ext
    assert urls[0]["name"].endswith("tar.xz")
    assert isinstance(build_number, int)
