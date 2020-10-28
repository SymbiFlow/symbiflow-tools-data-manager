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

import argparse
import json
import requests


# For now we use only `symbiflow-arch-defs` and download tarballs
def get_latest_artifact_url(
    project="symbiflow-arch-defs",
    build_name="install",
    jobset="continuous",
    get_max_int=False,
):
    # Handle case in which there is build_name is absent
    if build_name:
        build_name = f"/{build_name}"
    else:
        build_name = ""

    base_url = f"https://www.googleapis.com/storage/v1/b/{project}/o"
    prefix = f"artifacts/prod/foss-fpga-tools/{project}/{jobset}{build_name}/"
    params = {"prefix": prefix}
    urls_of_integers = {}

    to_strip = f"{project}/{prefix}"

    while True:
        r = requests.get(
            base_url,
            params=params,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()

        try:
            items = r.json()["items"]
        except KeyError as e:
            print(e)
            return ""

        for obj in items:
            obj_int = int(obj["id"].replace(to_strip, "").split("/")[0])
            urls_of_integers[obj_int] = obj["mediaLink"]

        try:
            params["pageToken"] = r.json()["nextPageToken"]
        except KeyError:
            break

    try:
        max_int = max(urls_of_integers.keys())
    except ValueError as e:
        print(e)
        return ""

    if get_max_int:
        return urls_of_integers[max_int], max_int
    else:
        return urls_of_integers[max_int]


def main():
    parser = argparse.ArgumentParser(
        description="Retrieves the latest artifacts of SymbiFlow-related CIs."
    )

    parser.add_argument(
        "--project",
        default="symbiflow-arch-defs",
        help="Name of the SymbiFlow project",
    )
    parser.add_argument(
        "--build_name",
        default="install",
        help="Name of the CI that produced the artifact",
    )
    parser.add_argument(
        "--jobset",
        default="continuous",
        help="Name of the jobset. Can choose between presubmit and continous",
    )
    parser.add_argument(
        "--get_max_int",
        action="store_true",
        help="Retrieve also the CI build number",
    )

    args = parser.parse_args()

    return get_latest_artifact_url(
        args.project, args.build_name, args.jobset, args.get_max_int
    )


if __name__ == "__main__":
    main()
