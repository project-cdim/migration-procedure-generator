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
"""pydantic data model"""

from jsonschema import ValidationError, validate
from pydantic import BaseModel, field_validator

from migration_procedure_generator.custom_exception import JsonSchemaError
from migration_procedure_generator.schema import layout_schema


class NodeLayout(BaseModel, extra="forbid"):
    """current layout and desired layout a data model to store the data"""

    currentLayout: dict
    desiredLayout: dict

    @field_validator("currentLayout")
    def validate_currentLayout(cls, currentLayout):  # pylint:disable=E0213,C0103
        """Validation checks for currentLayout

        Args:
            currentLayout (dict): Layout that performs validation checks

        Returns:
            dict: Layout with completed validation check
        """
        currentLayout = convert_devicetype_lowercase(currentLayout)
        validate_layout(currentLayout)

        return currentLayout

    @field_validator("desiredLayout")
    def validate_desiredLayout(cls, desiredLayout):  # pylint:disable=E0213,C0103
        """Validation checks for desiredLayout

        Args:
            desiredLayout (dict): Layout that performs validation checks

        Returns:
            dict: Layout with completed validation check
        """
        desiredLayout = convert_devicetype_lowercase(desiredLayout)
        validate_layout(desiredLayout)
        return desiredLayout


def validate_layout(layout: dict) -> None:
    """Validation checks for layout

    Args:
        layout (dict): Layout that performs validation checks
    """

    try:
        validate(layout, layout_schema)
    except ValidationError as err:
        raise JsonSchemaError(err.message) from err


def convert_devicetype_lowercase(layout: dict) -> dict:
    """Convert the device type key in layout to lowercase

    Args:
        layout (dict): Layout of the state received as a parameter

    Returns:
        layout (dict): Layout with the device type converted to lowercase
    """

    converted_data = layout.copy()
    nodes_devicetype_lowercase(layout, converted_data)
    bound_devices_devicetype_lowercase(layout, converted_data)
    return converted_data


def to_lowercase_keys(input_data):
    """Return a new dictionary with the keys in lowercase"""
    return {k.lower(): v for k, v in input_data.items()}


def nodes_devicetype_lowercase(layout: dict, converted_data: dict) -> None:
    """Convert the device type of nodes to lowercase.

    Args:
        layout (dict): ayout of the state received as a parameter
        converted_data (dict): Layout with the device type converted to lowercase
    """
    if "nodes" in layout and isinstance(layout.get("nodes"), list):
        lowercase_data = {"nodes": []}
        for node in layout["nodes"]:
            if "device" in node and isinstance(node.get("device"), dict):
                lowercase_data["nodes"].append({"device": to_lowercase_keys(node["device"])})
            else:
                lowercase_data["nodes"].append(node)
            converted_data.update(lowercase_data)


def bound_devices_devicetype_lowercase(layout: dict, converted_data: dict) -> None:
    """Convert the device type of boundDevices to lowercase.

    Args:
        layout (dict): ayout of the state received as a parameter
        converted_data (dict): Layout with the device type converted to lowercase
    """
    if "boundDevices" in layout and isinstance(layout.get("boundDevices"), dict):
        bound_device_lowercase_data = {"boundDevices": {}}
        for cpu_id, device_info in layout["boundDevices"].items():
            if callable(getattr(device_info, "items", None)):
                bound_device_lowercase_data["boundDevices"][cpu_id] = to_lowercase_keys(device_info)
                converted_data.update(bound_device_lowercase_data)
