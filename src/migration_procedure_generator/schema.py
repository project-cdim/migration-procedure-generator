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
"""jsonschema"""

config_schema = {
    "type": "object",
    "required": ["migration_procedures"],
    "description": "Configuration file for migration procedure",
    "properties": {
        "log": {
            "type": "object",
            "description": "Log definition",
            "properties": {
                "logging_level": {
                    "type": "string",
                    "description": "log level",
                    "enum": ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
                },
                "log_dir": {
                    "type": "string",
                    "description": "log directory",
                },
                "file": {
                    "type": "string",
                    "description": "log file name",
                },
                "rotation_size": {
                    "type": "integer",
                    "description": "log directory",
                },
                "backup_files": {
                    "type": "integer",
                    "description": "log file backup",
                },
                "stdout": {
                    "type": "boolean",
                    "description": "Log output will be displayed when true is specified, \
                    and also printed to the standard output.",
                },
            },
        },
        "migration_procedures": {
            "type": "object",
            "description": "Waiting setup for the API",
            "required": ["host", "port"],
            "properties": {
                "host": {
                    "type": "string",
                    "description": "IP address or host name to be used for the waiting process",
                },
                "port": {
                    "type": "integer",
                    "description": "Port number to be used for the waiting process",
                },
            },
        },
    },
}


layout_schema = {
    "type": "object",
    "description": "layout schema",
    "required": ["nodes"],
    "properties": {
        "nodes": {
            "type": "array",
            "description": "node",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "properties": {
                    "device": {
                        "type": "object",
                        "description": "device infomation",
                        "additionalProperties": False,
                        "required": ["cpu"],
                        "properties": {
                            "cpu": {
                                "type": "object",
                                "required": ["deviceIDs"],
                                "properties": {
                                    "deviceIDs": {
                                        "type": "array",
                                        "description": "cpu device ID",
                                        "maxItems": 1,
                                        "minItems": 1,
                                        "items": {"type": "string"},
                                    }
                                },
                            },
                        },
                        "patternProperties": {
                            "^(.+)$": {
                                "type": "object",
                                "required": ["deviceIDs"],
                                "properties": {
                                    "deviceIDs": {
                                        "type": "array",
                                        "description": "other device ID",
                                        "items": {"type": "string"},
                                    }
                                },
                            },
                        },
                    },
                },
            },
        },
        "boundDevices": {
            "description": "nonRemovable device",
            "type": "object",
            "patternProperties": {
                "^(.+)$": {
                    "type": "object",
                    "description": "device infomation",
                    "patternProperties": {
                        "^(.+)$": {
                            "type": "array",
                            "description": "nonRemovable device ID",
                            "items": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}
