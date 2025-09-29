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
import json

import pytest
from fastapi.testclient import TestClient

from migration_procedure_generator.custom_exception import SettingFileValidationError, LogSettingFileValidationError
from migration_procedure_generator.plan import Task
from migration_procedure_generator.server import app, main
from migration_procedure_generator.setting import MigrationConfigReader, MigrationLogConfigReader

client = TestClient(app)
BASEURL = "/cdim/api/v1/"


@pytest.fixture(scope="function", autouse=True)
def initializetask():
    """Initialize so that the test for other things doesn't affect it"""
    Task.__index_op_id__ = 0


class TestCreateMigrationProcedure:

    @pytest.mark.parametrize(
        "params,current_list",
        [
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory1": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory1": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage1": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 4,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 5,
                        "operation": "boot",
                        "dependencies": [4],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}},
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 3,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 4,
                        "operation": "boot",
                        "dependencies": [2, 3],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [{"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}}]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            },
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 2,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 3,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 4,
                        "operation": "boot",
                        "dependencies": [2, 3],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            },
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            },
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 3,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                    {
                        "operationID": 4,
                        "operation": "disconnect",
                        "dependencies": [3],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 5,
                        "operation": "connect",
                        "dependencies": [4, 1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 6,
                        "operation": "boot",
                        "dependencies": [5, 2],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 7,
                        "operation": "connect",
                        "dependencies": [2, 3],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 8,
                        "operation": "boot",
                        "dependencies": [7, 4],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            },
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                        ]
                                    },
                                }
                            },
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["D46DC8AB-E25B-AAE8-8B62-F72DD3A4EFC8"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
                                        ]
                                    },
                                }
                            },
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 3,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 4,
                        "operation": "disconnect",
                        "dependencies": [3],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 5,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                    {
                        "operationID": 6,
                        "operation": "disconnect",
                        "dependencies": [5],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 7,
                        "operation": "connect",
                        "dependencies": [6, 3],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 8,
                        "operation": "boot",
                        "dependencies": [7, 4],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 9,
                        "operation": "connect",
                        "dependencies": [4, 5],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 10,
                        "operation": "boot",
                        "dependencies": [9, 6],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                    {
                        "operationID": 11,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "D46DC8AB-E25B-AAE8-8B62-F72DD3A4EFC8",
                        "targetDeviceID": "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
                    },
                    {
                        "operationID": 12,
                        "operation": "boot",
                        "dependencies": [11],
                        "targetDeviceID": "D46DC8AB-E25B-AAE8-8B62-F72DD3A4EFC8",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {"nodes": []},
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {"nodes": []},
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 2,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 3,
                        "operation": "boot",
                        "dependencies": [1, 2],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {"nodes": []},
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 3,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {"nodes": []},
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 3,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {"nodes": []},
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 2,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 3,
                        "operation": "boot",
                        "dependencies": [1, 2],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {"deviceIDs": []},
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 2,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 5,
                        "operation": "boot",
                        "dependencies": [2],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {"deviceIDs": []},
                                    "storage": {"deviceIDs": []},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {"deviceIDs": []},
                                    "storage": {"deviceIDs": []},
                                    "gpu": {"deviceIDs": []},
                                    "networkInterface": {"deviceIDs": []},
                                }
                            }
                        ]
                    },
                },
                [],
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "nic": {
                                        "deviceIDs": [
                                            "1EA18953-68CD-41D6-8996-EAC8DDFB4E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 3,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "1EA18953-68CD-41D6-8996-EAC8DDFB4E3F",
                    },
                    {
                        "operationID": 5,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 6,
                        "operation": "boot",
                        "dependencies": [5, 3],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),  # unexpected value is specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                    "nic": {
                                        "deviceIDs": [
                                            "1EA18953-68CD-41D6-8996-EAC8DDFB4E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 4,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 5,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "1EA18953-68CD-41D6-8996-EAC8DDFB4E3F",
                    },
                    {
                        "operationID": 6,
                        "operation": "boot",
                        "dependencies": [4, 5],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                ],
            ),  # unexpected value is specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                            "55834ea0-bade-4ce0-89e0-c9fbc0ea7617",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ],
                        "boundDevices": {
                            "b477ea1c-db3d-48b3-9725-b0ce6e25efc2": {"memory": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"]}
                        },
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                    },
                    {
                        "operationID": 6,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                        "targetDeviceID": "8190c071-3f5f-4862-b741-b42591ac51fc",
                    },
                    {
                        "operationID": 7,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                        "targetDeviceID": "06ebec09-553a-462e-96f9-f58909180428",
                    },
                    {
                        "operationID": 8,
                        "operation": "boot",
                        "dependencies": [6, 7],
                        "targetDeviceID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                    },
                ],
            ),  # Memory is a built-in device.
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage1234567890": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu1234567890": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage1234567890": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                        "boundDevices": {
                            "b477ea1c-db3d-48b3-9725-b0ce6e25efc2": {
                                "memory": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"],
                                "storage1234567890": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"],
                                "networkInterface": ["8190c071-3f5f-4862-b741-b42591ac51fc"],
                                "gpu1234567890": ["06ebec09-553a-462e-96f9-f58909180428"],
                            }
                        },
                    },
                },
                [
                    {
                        "operationID": 1,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                    },
                    {
                        "operationID": 2,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 3,
                        "operation": "boot",
                        "dependencies": [2],
                        "targetDeviceID": "b477ea1c-db3d-48b3-9725-b0ce6e25efc2",
                    },
                ],
            ),  # Multiple internal devices
        ],
    )
    def test_create_migration_procedure_success(self, params, current_list):

        response = client.post(BASEURL + "migration-procedures", json=params)
        content = json.loads(response.content.decode())
        assert response.status_code == 200
        assert content == current_list
        assert response.charset_encoding == "utf-8"
        assert response.headers.get("X-Content-Type-Options") == "nosniff"

    @pytest.mark.parametrize(
        "params,msg",
        [
            (
                {
                    "currentLayout": {
                        "node": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'nodes' is a required property"),
            ),  # The 'nodes' in 'currentLayout' do not exist
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "node": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'nodes' is a required property"),
            ),  # The 'nodes' in 'desiredLayout' do not exist
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {
                                        "deviceIDs": [
                                            "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                                            "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                                        ]
                                    },
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is too long"),
            ),  # The deviceIDs of the cpu key contains more than one value
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {
                                        "deviceIDs": [
                                            "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                                            "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                                        ]
                                    },
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is too long"),
            ),  # The deviceIDs of the cpu key contains more than one value
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is a required property"),
            ),  # No CPU detected
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is a required property"),
            ),  # No CPU detected
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memory": {
                                    "deviceIDs": [
                                        "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                    ]
                                },
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("Additional properties are not allowed"),
            ),  # No device detected
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memory": {
                                    "deviceIDs": [
                                        "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                    ]
                                },
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        ]
                    },
                },
                ("Additional properties are not allowed"),
            ),  # No device detected
            (
                {
                    "currentLayout": {"nodes": [{"device": {}}]},
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'cpu' is a required property"),
            ),  # NO cpu detected
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {"nodes": [{"device": {}}]},
                },
                ("'cpu' is a required property"),
            ),  # NO cpu detected
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": [1]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is not of type 'string'"),
            ),  # A string is not specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": [1]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is not of type 'string'"),
            ),  # A string is not specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            1,
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is not of type 'string'"),
            ),  # A string is not specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {"deviceIDs": [1]},
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is not of type 'string'"),
            ),  # A string is not specified
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "node": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'nodes' is a required property"),
            ),  # The 'nodes' in 'desiredLayout' do not exist
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "node": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'nodes' is a required property"),
            ),  # The 'deviceIDs' in 'desiredLayout' do not exist
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "gpu": {"deviceIDs": []},
                                    "storage": {},
                                }
                            }
                        ]
                    },
                },
                ("'deviceIDs' is a required property"),
            ),  # The 'deviceIDs' in 'desiredLayout' do not exist
            (
                {
                    "currentLayout": {"nodes": [{"device": {"cpu": {"deviceIDs": []}}}]},
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ]
                    },
                },
                ("should be non-empty"),
            ),
            (
                {
                    "currentLayout": {"nodes": [{"device": {"cpu": {}}}]},
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ]
                    },
                },
                ("'deviceIDs' is a required property"),
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": [1]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("is not of type 'string'"),
            ),
            (
                {
                    "currentLayout": {
                        "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                        "memory": {
                            "deviceIDs": [
                                "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                            ]
                        },
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "memory": {
                                        "deviceIDs": [
                                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                        ]
                                    },
                                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                }
                            }
                        ]
                    },
                },
                ("'nodes' is a required property"),
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                        "boundDevices": {
                            "memory": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"],
                            "storage": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"],
                            "networkInterface": ["8190c071-3f5f-4862-b741-b42591ac51fc"],
                            "gpu": ["06ebec09-553a-462e-96f9-f58909180428"],
                        },
                    },
                },
                "['7fd3301f-9a1d-4652-86d6-1fa84cf55f5b'] is not of type 'object'",
            ),  # Multiple internal devices
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                        "boundDevices": [],
                    },
                },
                "[] is not of type 'object'",
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                        "boundDevices": {
                            "b477ea1c-db3d-48b3-9725-b0ce6e25efc2": {
                                "memory": {"deciesIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"]}
                            }
                        },
                    },
                },
                "{'deciesIDs': ['895DFB43-68CD-41D6-8996-EAC8D1EA1E3F']} is not of type 'array'",
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "network-Interface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                    },
                },
                "'network-interface' does not match any of the regexes: '^[0-9a-zA-Z]+$'",
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                    "network-Interface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                }
                            }
                        ],
                    },
                },
                "'network-interface' does not match any of the regexes: '^[0-9a-zA-Z]+$'",
            ),
            (
                {
                    "currentLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "memory": {"deviceIDs": ["55834ea0-bade-4ce0-89e0-c9fbc0ea7617"]},
                                    "storage": {"deviceIDs": ["7fd3301f-9a1d-4652-86d6-1fa84cf55f5b"]},
                                    "networkInterface": {"deviceIDs": ["8190c071-3f5f-4862-b741-b42591ac51fc"]},
                                    "gpu": {"deviceIDs": ["06ebec09-553a-462e-96f9-f58909180428"]},
                                }
                            }
                        ]
                    },
                    "desiredLayout": {
                        "nodes": [
                            {
                                "device": {
                                    "cpu": {"deviceIDs": ["b477ea1c-db3d-48b3-9725-b0ce6e25efc2"]},
                                    "storage": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                }
                            }
                        ],
                        "boundDevices": {
                            "b477ea1c-db3d-48b3-9725-b0ce6e25efc2": {
                                "memory": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"],
                                "networkInterface": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"],
                                "network-Interface": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"],
                            }
                        },
                    },
                },
                "'network-interface' does not match any of the regexes: '^[0-9a-zA-Z]+$'",
            ),
        ],
    )
    def test_create_migration_procedure_failure_when_validation_error(self, params, msg):
        response = client.post(BASEURL + "migration-procedures", json=params)
        content = json.loads(response.content.decode())
        assert response.status_code == 400
        assert "E50001" in content.get("code")
        assert msg in content.get("message")

    @pytest.mark.parametrize("name", [("desiredLayout"), ("currentLayout")])
    def test_create_migration_procedure_failure_when_only_one_layout(self, name):
        params = {
            name: {
                "nodes": [
                    {
                        "device": {
                            "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                            "memory": {
                                "deviceIDs": [
                                    "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                ]
                            },
                        }
                    }
                ]
            },
        }

        response = client.post(BASEURL + "migration-procedures", json=params)
        assert response.status_code == 400
        assert "body" in response.content.decode()
        assert name in response.content.decode()
        assert "E50001" in response.content.decode()

    @pytest.mark.parametrize(
        "param1, param2",
        [("beforeLayout", "desiredLayout"), ("currentLayout", "afterLayout"), ("beforeLayout", "afterLayout")],
    )
    def test_create_migration_procedure_failure_key_name_before_fix(self, param1, param2):
        params = {
            param1: {"nodes": []},
            param2: {"nodes": []},
        }

        response = client.post(BASEURL + "migration-procedures", json=params)
        assert response.status_code == 400
        assert "body" in response.content.decode()
        assert "E50001" in response.content.decode()

    def test_create_migration_procedure_failure_when_config_error_log_none(self, mocker):

        params = {
            "currentLayout": {"nodes": []},
            "desiredLayout": {"nodes": []},
        }
        mocker.patch("migration_procedure_generator.server.initialize_log").side_effect = LogSettingFileValidationError(
            "Dummy message"
        )
        response = client.post(BASEURL + "migration-procedures", json=params)
        content = json.loads(response.content.decode())
        assert response.status_code == 500
        assert "E50005" in content.get("code")
        assert "Failed to load migrationprocedures_log_config.yaml\nDummy message" in content.get("message")

    def test_create_migration_procedure_failure_when_config_error_calllog(self, mocker):

        params = {
            "currentLayout": {"nodes": []},
            "desiredLayout": {"nodes": []},
        }

        mocker.patch("migration_procedure_generator.server.Plan.system_update_plan").side_effect = (
            SettingFileValidationError("Dummy message")
        )
        response = client.post(BASEURL + "migration-procedures", json=params)
        content = json.loads(response.content.decode())
        assert response.status_code == 500
        assert "E50005" in content.get("code")
        assert "Failed to load migrationprocedures_config.yaml\nDummy message" in content.get("message")

    def test_create_migration_procedure_failure_when_log_initialization_error_calllog(self, mocker):
        """abnormal system testing"""
        config = {
                'version': 1,
                'formatters': {
                    'standard': {
                        'format': "%(asctime)s %(levelname)s %(message)s",
                        'datefmt': "%Y/%m/%d %H:%M:%S.%f"
                    }
                },
                'handlers': {
                    'file': {
                        'class': 'logging.handlers.RotatingFileHandler',
                        'level': 'INFO',
                        'formatter': 'standard',
                        'filename': 'internal_server_error/app_layout_apply.log',
                        'maxBytes': 100000000,
                        'backupCount': 72,
                    },
                    'console': {
                        'class': 'logging.StreamHandler',
                        'level': 'INFO',
                        'formatter': 'standard',
                        'stream': 'ext://sys.stdout'
                    }
                },
                'root': {
                    'level': 'INFO',
                    'handlers': ['file']
                }
        }
        mocker.patch("yaml.safe_load").return_value = config
        mocker.patch.object(MigrationLogConfigReader, "_check_directory_exists")
        params = {
            "currentLayout": {"nodes": []},
            "desiredLayout": {"nodes": []},
        }
        response = client.post(BASEURL + "migration-procedures", json=params)
        content = json.loads(response.content.decode())
        assert response.status_code == 500
        assert "E50006" in content.get("code")
        assert "Internal server error. Failed in log initialization." in content.get("message")

    @pytest.mark.parametrize(
        "params",
        [
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memory": {"deviceIDs": []},
                                "storage": {"deviceIDs": []},
                                "gpu": {"deviceIDs": []},
                                "networkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # base key name
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "CPU": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "MEMORY": {"deviceIDs": []},
                                "STORAGE": {"deviceIDs": []},
                                "GPU": {"deviceIDs": []},
                                "NETWORKINTERFACE": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # all uppercase
            },
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "Cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "Memory": {"deviceIDs": []},
                                "Storage": {"deviceIDs": []},
                                "Gpu": {"deviceIDs": []},
                                "NetworkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # first letter is capitalized
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cpU": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memorY": {"deviceIDs": []},
                                "storagE": {"deviceIDs": []},
                                "gpU": {"deviceIDs": []},
                                "networkInterfacE": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # last letter is capitalized
            },
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "Cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "Memory": {"deviceIDs": []},
                                "Storage": {"deviceIDs": []},
                                "Gpu": {"deviceIDs": []},
                                "NetworkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # first letter is capitalized
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cPu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "mEmOrY": {"deviceIDs": []},
                                "StOrAgE": {"deviceIDs": []},
                                "GpU": {"deviceIDs": []},
                                "nEtWoRkInTeRfAcE": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # The upper and lower case letters alternate with each character
            },
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memory": {"deviceIDs": []},
                                "storage": {"deviceIDs": []},
                                "gpu": {"deviceIDs": []},
                                "networkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # base key name
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "CPU": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "MEMORY": {"deviceIDs": []},
                                "STORAGE": {"deviceIDs": []},
                                "GPU": {"deviceIDs": []},
                                "NETWORKINTERFACE": {"deviceIDs": []},
                            }
                        }
                    ],
                    "boundDevices": {
                        "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA": {
                            "MEMORY": ["388e64e3-efa7-484c-b63c-28bf1709d6c1"],
                            "STORAGE": ["33f19666-68b3-4ed7-a9a8-d046f0879ff2"],
                            "GPU": ["06ebec09-553a-462e-96f9-f58909180428"],
                            "NETWORKINTERFACE": ["8d45fffa-e7f5-462f-88d3-94ef9b46a8ab"],
                        }
                    },
                },  # all uppercase
            },
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "Cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "Memory": {"deviceIDs": []},
                                "Storage": {"deviceIDs": []},
                                "Gpu": {"deviceIDs": []},
                                "NetworkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # first letter is capitalized
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cpU": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "memorY": {"deviceIDs": []},
                                "storagE": {"deviceIDs": []},
                                "gpU": {"deviceIDs": []},
                                "networkInterfacE": {"deviceIDs": []},
                            }
                        }
                    ],
                    "boundDevices": {
                        "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA": {
                            "memorY": ["388e64e3-efa7-484c-b63c-28bf1709d6c1"],
                            "storagE": ["33f19666-68b3-4ed7-a9a8-d046f0879ff2"],
                            "gpU": ["06ebec09-553a-462e-96f9-f58909180428"],
                            "networkInterfacE": ["8d45fffa-e7f5-462f-88d3-94ef9b46a8ab"],
                        }
                    },
                },  # last letter is capitalized
            },
            {
                "currentLayout": {
                    "nodes": [
                        {
                            "device": {
                                "Cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "Memory": {"deviceIDs": []},
                                "Storage": {"deviceIDs": []},
                                "Gpu": {"deviceIDs": []},
                                "NetworkInterface": {"deviceIDs": []},
                            }
                        }
                    ]
                },  # first letter is capitalized
                "desiredLayout": {
                    "nodes": [
                        {
                            "device": {
                                "cPu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                                "mEmOrY": {"deviceIDs": []},
                                "StOrAgE": {"deviceIDs": []},
                                "GpU": {"deviceIDs": []},
                                "nEtWoRkInTeRfAcE": {"deviceIDs": []},
                            }
                        }
                    ],
                    "boundDevices": {
                        "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA": {
                            "mEmOrY": ["388e64e3-efa7-484c-b63c-28bf1709d6c1"],
                            "StOrAgE": ["33f19666-68b3-4ed7-a9a8-d046f0879ff2"],
                            "GpU": ["06ebec09-553a-462e-96f9-f58909180428"],
                            "nEtWoRkInTeRfAcE": ["8d45fffa-e7f5-462f-88d3-94ef9b46a8ab"],
                        }
                    },
                },  # The upper and lower case letters alternate with each character
            },
        ],
    )
    def test_create_migration_procedure_success_when_key_name_are_case_insensitive(self, params):
        response = client.post(BASEURL + "migration-procedures", json=params)

        assert response.status_code == 200


class TestMain:
    def test_main_failure_when_load_config_file(self, mocker, capfd):
        mocker.patch(
            "migration_procedure_generator.server.MigrationConfigReader",
            side_effect=SettingFileValidationError("Failed to load migrationprocedures_config.yaml"),
        )
        main()
        _, err = capfd.readouterr()
        assert err.split("\n")[0] == "[E50005]Failed to load migrationprocedures_config.yaml"

    def test_main_when_no_traceback_desired_server(self, mocker):
        mockup = mocker.patch("migration_procedure_generator.server.uvicorn.run", side_effect=KeyboardInterrupt)

        # Test execution
        main()

        assert mockup.call_count == 1
