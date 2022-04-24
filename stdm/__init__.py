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

import argparse
import json
import requests


# For now we use only `symbiflow-arch-defs` and download tarballs
def get_latest_artifact_url(project="symbiflow-arch-defs", build_name="install", jobset="continuous"):
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
            if obj_int not in urls_of_integers:
                urls_of_integers[obj_int] = list()

            artifact_name = obj["selfLink"].split("%2F")[-1]
            artifact_link = obj["mediaLink"]
            artifact = {"name": artifact_name, "url": obj["mediaLink"]}
            urls_of_integers[obj_int].append(artifact)

        try:
            params["pageToken"] = r.json()["nextPageToken"]
        except KeyError:
            break

    try:
        max_int = max(urls_of_integers.keys())
    except ValueError as e:
        print(e)
        return ""

    return urls_of_integers[max_int], max_int


def main():
    parser = argparse.ArgumentParser(description="Retrieves the latest artifacts of SymbiFlow-related CIs.")

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
        "--get_build_number",
        action="store_true",
        help="Retrieve the CI build number",
    )
    parser.add_argument(
        "--get_single_url",
        action="store_true",
        help="Retrieve a single random URL from a given build",
    )
    parser.add_argument(
        "--get_all_urls",
        action="store_true",
        help="Retrieve all the URLs of a given build",
    )

    args = parser.parse_args()

    # Default to use get_single_url if none of the options is selected
    if not (args.get_all_urls or args.get_single_url or args.get_build_number):
        args.get_single_url = True

    if args.get_build_number:
        assert not (args.get_all_urls or args.get_single_url)
        _, build_number = get_latest_artifact_url(args.project, args.build_name, args.jobset)
        print(build_number)

    elif args.get_all_urls:
        assert not (args.get_build_number or args.get_single_url)
        urls, _ = get_latest_artifact_url(args.project, args.build_name, args.jobset)
        for url in urls:
            print(url)

    elif args.get_single_url:
        assert not (args.get_build_number or args.get_all_urls)
        urls, _ = get_latest_artifact_url(args.project, args.build_name, args.jobset)
        print(urls[0]["url"])


if __name__ == "__main__":
    main()
