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

log_config_schema = {
    "type": "object",
    "required": ["version", "formatters", "handlers", "root"],
    "properties": {
        "version": {"type": "integer"},
        "formatters": {
            "type": "object",
            "properties": {
                "standard": {
                    "type": "object",
                    "properties": {"format": {"type": "string"}, "datefmt": {"type": "string"}},
                    "required": ["format", "datefmt"],
                }
            },
            "required": ["standard"],
        },
        "handlers": {
            "type": "object",
            "properties": {
                "file": {
                    "type": "object",
                    "properties": {
                        "class": {"type": "string"},
                        "level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
                        },
                        "formatter": {"type": "string"},
                        "filename": {"type": "string"},
                        "maxBytes": {"type": "integer"},
                        "backupCount": {"type": "integer"},
                        "encoding": {"type": "string"},
                    },
                    "required": ["class", "formatter", "filename", "maxBytes", "backupCount"],
                },
                "console": {
                    "type": "object",
                    "properties": {
                        "class": {"type": "string"},
                        "level": {
                            "type": "string",
                            "enum": ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
                        },
                        "formatter": {"type": "string"},
                        "stream": {"type": "string"},
                    },
                    "required": ["class", "formatter", "stream"],
                },
            },
            "required": ["file"],
        },
        "root": {
            "type": "object",
            "properties": {
                "level": {
                    "type": "string",
                    "enum": ["DEBUG", "INFO", "WARN", "ERROR", "CRITICAL"],
                },
                "handlers": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["level", "handlers"],
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
                            "^[0-9a-zA-Z]+$": {
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
                        "^[0-9a-zA-Z]+$": {
                            "type": "array",
                            "description": "nonRemovable device ID",
                            "items": {"type": "string"},
                        },
                    },
                    "additionalProperties": False,
                },
            },
            "additionalProperties": False,
        },
    },
}
