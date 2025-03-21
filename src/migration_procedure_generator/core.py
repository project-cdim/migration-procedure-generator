# Copyright (C) 2025 NEC Corporation.
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
#  under the License.
"""CLI package"""

import argparse
import json
import sys

from migration_procedure_generator.custom_exception import (
    CustomBaseException,
    FileReadError,
    JSONDecodeError,
    NotFoundError,
)
from migration_procedure_generator.exitcode import ExitCode
from migration_procedure_generator.model import validate_layout, convert_devicetype_lowercase
from migration_procedure_generator.plan import Plan
from migration_procedure_generator.setting import initialize_log
from migration_procedure_generator.system import System


def get_validate_json_file(file_path) -> dict:
    """_Checking for validaty of json file

    Args:
        file_path (str): File path that has been loaded

    Raises:
        JSONDecodeError: this error gonna be throw when FileFormatError has been occured
        NotFoundError: this error gonna be throw when FileNotFound has been occured
        FileReadError: this error gonna be throw when PermissionError has been occured

    Returns:
        dict: json loaded object
    """

    try:
        with open(file_path, "r", encoding="UTF-8") as fh:
            return json.load(fh)
    except json.JSONDecodeError as err:
        raise JSONDecodeError() from err
    except FileNotFoundError as err:
        raise NotFoundError(file_path) from err
    except Exception as err:
        raise FileReadError(file_path) from err


def main():
    """entry point"""
    cli_parser = argparse.ArgumentParser(description="generate a system update plan")
    cli_parser.add_argument(
        "--prev",
        action="store",
        type=str,
        required=True,
        help="Path of a previous system file in JSON format",
        metavar="CURRENT_LAYOUT_FILE",
    )

    cli_parser.add_argument(
        "--new",
        action="store",
        type=str,
        required=True,
        help="Path of a new system file in JSON format",
        metavar="DESIRED_LAYOUT_FILE",
    )

    args = cli_parser.parse_args()

    try:
        logger = initialize_log()
        prev_data = convert_devicetype_lowercase(get_validate_json_file(args.prev))
        new_data = convert_devicetype_lowercase(get_validate_json_file(args.new))
        validate_layout(prev_data)
        validate_layout(new_data)
        logger.info("Start running")
        logger.info(f"input param prev:{prev_data}, new:{new_data}")
    except CustomBaseException as err:
        err.output_stderr()
        sys.exit(err.exit_code)
    bound_devices_map = new_data.get("boundDevices", {})
    plan = Plan.system_update_plan(
        System.decode_json(prev_data, bound_devices_map), System.decode_json(new_data, bound_devices_map)
    )
    logger.info("Completed successfully")
    print(json.dumps(plan.encode_json()))
    sys.exit(ExitCode.NORMAL)


if __name__ == "__main__":
    main()  # pragma: no cover
