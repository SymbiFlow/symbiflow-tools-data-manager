# SymbiFlow tools data manager (STDM)

This python package is used to retrieve the latest artifacts stored in Google Cloude Storage (GCS).
The artifacts are uploaded by the SymbiFlow projects CI builds.

## Usage

This script has four optional parameters to control which bucket and which artifact to get:

- `--project`: name of the project/repository within the SymbiFlow organization. (default `symbiflow-arch-defs`)
- `--build_name`: name of the CI that has uploaded the desired artifact. (default `install`)
- `--jobset`: name of the jobset. This can assume two values: `presubmit`, `continuous` (default).
- `--get_max_int`: option to return also the number of the latest build. (default `False`)
