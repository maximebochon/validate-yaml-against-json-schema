#!/usr/bin/env python3
#
# Author: Maxime BOCHON
# E-mail: maxime.bochon@gmail.com
# Created: 2019-04-04
# Version: 2019-04-23
#
# Requirements (Debian Linux syntax):
#  sudo apt install python3-pip
#  pip3 install jsonschema
#  pip3 install pyyaml


# Imports
import argparse
import yaml
import json
import jsonschema

from enum import IntEnum
from sys import stderr, stdout, exit
from jsonschema.exceptions import SchemaError, ValidationError


# Exit codes
class ExitCode(IntEnum):
    VALID_DOCUMENT = 0
    INVALID_DOCUMENT = 10
    INVALID_SCHEMA = 11
    LOAD_DOCUMENT_ERROR = 20
    LOAD_SCHEMA_ERROR = 21
    UNEXPECTED_ERROR = 1


# Argument handling
parser = argparse.ArgumentParser(description="Validate a YAML document against a JSON schema.")
parser.add_argument("-d", "--document", "--yaml-document", help="Path to the YAML document to validate", required=True)
parser.add_argument("-s", "--schema", "--json-schema", help="Path to the JSON schema used for validation", required=True)
parser.add_argument("-q", "--quiet", "--quiet-mode", help="Do not display any error or success message", action="store_true")
args = parser.parse_args()


# Load JSON schema
try:
    with open(args.schema, "r") as schema_file:
        schema = json.load(schema_file)
except Exception as e:
    if not args.quiet:
        print("Error loading JSON schema: ", e, file=stderr)
    exit(ExitCode.LOAD_SCHEMA_ERROR)


# Load YAML document
try:
    with open(args.document, "r") as document_file:
        document = yaml.safe_load(document_file)
except Exception as e:
    if not args.quiet:
        print("Error loading YAML document: ", e, file=stderr)
    exit(ExitCode.LOAD_DOCUMENT_ERROR)


# Validate YAML document against JSON schema
try:
    jsonschema.validate(instance=document, schema=schema)
    if not args.quiet:
        print('YAML document is valid against JSON schema.', file=stdout)
    exit(ExitCode.VALID_DOCUMENT)
except ValidationError as e:
    if not args.quiet:
        print("Error in YAML document: ", e, file=stderr)
    exit(ExitCode.INVALID_DOCUMENT)
except SchemaError as e:
    if not args.quiet:
        print("Error in JSON schema: ", e, file=stderr)
    exit(ExitCode.INVALID_SCHEMA)
