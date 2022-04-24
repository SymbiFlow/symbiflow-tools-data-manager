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

import os
from setuptools import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="stdm",
    version="0.1",
    author="SymbiFlow Authors",
    author_email="symbiflow@lists.librecores.org",
    description="SymbiFlow Tools Data Manager",
    python_requires=">=3.6",
    url="https://github.com/SymbiFlow/symbiflow-tools-data-manager.git",
    entry_points={"console_scripts": ["symbiflow_get_latest_artifact_url=stdm.__init__:main"]},
    install_requires=[
        "requests",
    ],
    license="Apache-2.0",
    long_description=read("README.md"),
    packages=["stdm"],
)
