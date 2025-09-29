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
import pytest

from migration_procedure_generator.plan import Plan, Task
from migration_procedure_generator.system import System


@pytest.fixture(scope="function", autouse=True)
def initializetask():
    # Initialize so that the test for other things doesn't affect it
    Task.__index_op_id__ = 0


class TestTask:
    def test_task_success_create_shutdown_task(self):
        current_json = {
            "operationID": 1,
            "operation": "shutdown",
            "dependencies": [],
            "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
        }
        task = Task(
            operation="shutdown", cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6", device_id=None, dependencies=None
        )
        assert task.operation == "shutdown"
        assert task.cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert task.device_id is None
        assert task.dependencies == []
        assert task.op_id == 1
        assert task.get_all_dependencies() == []
        assert task.encode_json() == current_json

    def test_task_success_create_boot_task(self):
        current_json = {
            "operationID": 1,
            "operation": "boot",
            "dependencies": [],
            "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
        }
        task = Task(operation="boot", cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6", device_id=None, dependencies=None)
        assert task.operation == "boot"
        assert task.cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert task.device_id is None
        assert task.dependencies == []
        assert task.op_id == 1
        assert task.get_all_dependencies() == []
        assert task.encode_json() == current_json

    def test_task_success_create_disconnect_task(self):
        current_json = {
            "operationID": 1,
            "operation": "disconnect",
            "dependencies": [],
            "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
        }
        task = Task(
            operation="disconnect",
            cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            device_id="895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            dependencies=None,
        )
        assert task.operation == "disconnect"
        assert task.cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert task.device_id == "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"
        assert task.dependencies == []
        assert task.op_id == 1
        assert task.get_all_dependencies() == []
        assert task.encode_json() == current_json

    def test_task_success_create_connect_task(self):
        current_json = {
            "operationID": 1,
            "operation": "connect",
            "dependencies": [],
            "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
        }
        task = Task(
            operation="connect",
            cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            device_id="2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
            dependencies=None,
        )
        assert task.operation == "connect"
        assert task.cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert task.device_id == "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"
        assert task.dependencies == []
        assert task.op_id == 1
        assert task.get_all_dependencies() == []
        assert task.encode_json() == current_json

    def test_task_success_create_connect_task_when_deviceid_is_none(self):
        current_json = {
            "operationID": 1,
            "operation": "connect",
            "dependencies": [],
            "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
        }
        task = Task(
            operation="connect", cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6", device_id=None, dependencies=None
        )
        assert task.operation == "connect"
        assert task.cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert task.device_id is None
        assert task.dependencies == []
        assert task.op_id == 1
        assert task.get_all_dependencies() == []
        assert task.encode_json() == current_json

    def test_task_encode_json_success(self):
        current_json = {
            "operationID": 1,
            "operation": "connect",
            "dependencies": [],
            "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            "targetDeviceID": "1985DE3F-18C6-46D6-D989-1EAFBAE8DC43",
        }
        task = Task(
            operation="connect",
            cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            device_id="1985DE3F-18C6-46D6-D989-1EAFBAE8DC43",
            dependencies=None,
        )
        task_json = task.encode_json()
        assert task_json == current_json

    def test_task_equal_success(self):
        task_boot_cpu1 = Task(
            operation="shutdown", cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6", device_id=None, dependencies=None
        )
        task_boot_cpu2 = Task(
            operation="shutdown", cpu_id="EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA", device_id=None, dependencies=None
        )
        assert task_boot_cpu1 != 1
        assert task_boot_cpu1 != task_boot_cpu2
        assert task_boot_cpu1 < task_boot_cpu2


class TestPlan:

    def test_plan_append_success(self):
        plan = Plan([])
        shutdown_task = Task(operation="shutdown", cpu_id="3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6", dependencies=[])
        plan.append(shutdown_task)

        current_list = [
            {
                "operationID": 1,
                "operation": "shutdown",
                "dependencies": [],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            }
        ]
        assert plan.encode_json() == current_list

    def test_plan_extend_success(self):
        prev = {
            "nodes": [
                {"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}},
            ],
        }
        bound_devices_map = {}

        plan = Plan([])
        system_list = System.decode_json(prev, bound_devices_map)
        dest_plan = plan.system_destruct_plan(system_list)
        plan.extend(dest_plan)

        current_list = [
            {
                "operationID": 1,
                "operation": "shutdown",
                "dependencies": [],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            }
        ]
        assert plan.encode_json() == current_list

    def test_plan_remove_success(self):
        prev = {
            "nodes": [
                {"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}},
            ]
        }
        bound_devices_map = {}
        plan = Plan([])
        system_list = System.decode_json(prev, bound_devices_map)
        dest_plan = plan.system_destruct_plan(system_list)
        plan.extend(dest_plan)

        current_list = [
            {
                "operationID": 1,
                "operation": "shutdown",
                "dependencies": [],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            }
        ]
        assert plan.encode_json() == current_list
        for task in dest_plan.tasks:
            plan.remove(task)
        assert plan.tasks == []

    def test_plan_encode_json_success(self):
        prev = {"nodes": []}
        new = {
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
        }
        bound_devices_map = {}

        plans = Plan.system_update_plan(
            System.decode_json(prev, bound_devices_map), System.decode_json(new, bound_devices_map)
        )
        current_list = [
            {
                "operationID": 1,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            },
            {
                "operationID": 2,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            },
            {
                "operationID": 3,
                "operation": "boot",
                "dependencies": [1, 2],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            },
        ]
        assert plans.encode_json() == current_list

    def test_plan_device_slice_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        bound_devices_map = {}
        plans = Plan.system_update_plan(
            System.decode_json(prev, bound_devices_map), System.decode_json(new, bound_devices_map)
        )

        assert plans.device_slice("895DFB43-68CD-41D6-8996-EAC8D1EA1E3F")[0].op_id == 3
        assert plans.device_slice("895DFB43-68CD-41D6-8996-EAC8D1EA1E3F")[0].operation == "connect"
        assert (
            plans.device_slice("895DFB43-68CD-41D6-8996-EAC8D1EA1E3F")[0].cpu_id
            == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        )
        assert (
            plans.device_slice("895DFB43-68CD-41D6-8996-EAC8D1EA1E3F")[0].device_id
            == "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"
        )

    def test_plan_cpu_slice_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }
        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
        assert plans.cpu_slice("3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6")[0].op_id == 1
        assert plans.cpu_slice("3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6")[0].operation == "shutdown"
        assert (
            plans.cpu_slice("3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6")[0].cpu_id == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        )
        assert plans.cpu_slice("3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6")[0].dependencies == []

    def test_plan_get_all_cpus_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
        assert "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6" in plans.get_all_cpus()

    def test_plan_get_all_devices_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
        assert "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F" in plans.get_all_devices()
        assert "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F" in plans.get_all_devices()
        assert "5DFB4893-C16D-4968-89D6-8D1EAECEA31F" in plans.get_all_devices()

    def test_plan_get_shutdown_tasks_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
        assert "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6" in plans.get_shutdown_tasks().keys()

    def test_get_boot_tasks_success(self):
        new = {
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
        }
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
        assert "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6" in plans.get_boot_tasks().keys()

    def test_plan_complete_device_dependencies_success(self):
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plan = Plan([])
        system_list = System.decode_json(prev, {})
        dest_plan = plan.system_destruct_plan(system_list)
        const_plan = plan.system_construct_plan(system_list)
        plan.extend(dest_plan)
        plan.extend(const_plan)

        plan.complete_device_dependencies()

        assert plan.tasks[0].encode_json()["dependencies"] == []
        assert plan.tasks[1].encode_json()["dependencies"] == [1]
        assert plan.tasks[2].encode_json()["dependencies"] == [2, 1]
        assert plan.tasks[3].encode_json()["dependencies"] == [3, 2]

        plan.complete_device_dependencies()

        assert plan.tasks[0].encode_json()["dependencies"] == []
        assert plan.tasks[1].encode_json()["dependencies"] == [1]
        assert plan.tasks[2].encode_json()["dependencies"] == [2, 1, 2]
        assert plan.tasks[3].encode_json()["dependencies"] == [3, 2]

    def test_plan_remove_redundant_success(self):
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plan = Plan([])
        system_list = System.decode_json(prev, {})
        dest_plan = plan.system_destruct_plan(system_list)
        const_plan = plan.system_construct_plan(system_list)
        plan.extend(dest_plan)
        plan.extend(const_plan)

        plan.remove_redundant_tasks()

        assert plan.tasks == []

    def test_plan_remove_indirect_dependencies_success(self):
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plan = Plan([])
        system_list = System.decode_json(prev, {})
        dest_plan = plan.system_destruct_plan(system_list)
        const_plan = plan.system_construct_plan(system_list)
        plan.extend(const_plan)
        plan.extend(dest_plan)
        plan.complete_device_dependencies()
        plan.remove_indirect_dependencies()
        assert plan.tasks[0].encode_json()["dependencies"] == []
        assert plan.tasks[1].encode_json()["dependencies"] == [1]
        assert plan.tasks[2].encode_json()["dependencies"] == [2]
        assert plan.tasks[3].encode_json()["dependencies"] == [3]

    def test_plan_system_destruct_success(self):
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plan = Plan([])
        system_list = System.decode_json(prev, {})
        node = plan.system_destruct_plan(system_list)
        current_list = [
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
                "targetDeviceID": "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
            },
        ]
        assert node.encode_json() == current_list

    def test_plan_node_destruct_success(self):
        prev = {
            "nodes": [
                {
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                    }
                },
            ]
        }

        plan = Plan([])
        system_list = System.decode_json(prev, {})
        node = plan.node_destruct_plan(system_list.nodes[0])
        current_list = [
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
                "targetDeviceID": "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
            },
        ]
        assert node.encode_json() == current_list

    def test_plan_system_construct_plan_success(self):
        new = {
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
        }
        plan = Plan([])
        system_list = System.decode_json(new, {})
        node = plan.system_construct_plan(system_list)
        current_list = [
            {
                "operationID": 1,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            },
            {
                "operationID": 2,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            },
            {
                "operationID": 3,
                "operation": "boot",
                "dependencies": [1, 2],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            },
        ]
        assert node.encode_json() == current_list

    def test_plan_node_construct_plan_success(self):
        new = {
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
        }
        plan = Plan([])
        system_list = System.decode_json(new, {})
        node = plan.node_construct_plan(system_list.nodes[0])
        current_list = [
            {
                "operationID": 1,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            },
            {
                "operationID": 2,
                "operation": "connect",
                "dependencies": [],
                "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            },
            {
                "operationID": 3,
                "operation": "boot",
                "dependencies": [1, 2],
                "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
            },
        ]
        assert node.encode_json() == current_list

    @pytest.mark.parametrize(
        "new,prev,current_list",
        [
            (
                {
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
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "memory": {"deviceIDs": ["C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F"]},
                            }
                        },
                    ]
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
                        "targetDeviceID": "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
                    },
                    {
                        "operationID": 3,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 4,
                        "operation": "connect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 5,
                        "operation": "boot",
                        "dependencies": [3, 4, 2],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                ],
            ),
            (
                {
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
                {"nodes": []},
                [
                    {
                        "operationID": 1,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 2,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 3,
                        "operation": "boot",
                        "dependencies": [1, 2],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                ],
            ),
            (
                {"nodes": []},
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {
                                    "deviceIDs": [
                                        "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                                        "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                    ]
                                },
                            }
                        },
                    ]
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
                    {
                        "operationID": 3,
                        "operation": "disconnect",
                        "dependencies": [1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                ],
            ),
            ({"nodes": []}, {"nodes": []}, []),
            (
                {
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
                {
                    "nodes": [
                        {"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}},
                    ]
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
                {"nodes": [{"device": {"cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]}}}]},
                {
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
                {
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
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                    {
                        "operationID": 4,
                        "operation": "disconnect",
                        "dependencies": [3],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 5,
                        "operation": "connect",
                        "dependencies": [4, 1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
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
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
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
                {
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
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                    {
                        "operationID": 4,
                        "operation": "disconnect",
                        "dependencies": [3],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 5,
                        "operation": "shutdown",
                        "dependencies": [],
                        "targetDeviceID": "D46DC8AB-E25B-AAE8-8B62-F72DD3A4EFC8",
                    },
                    {
                        "operationID": 6,
                        "operation": "disconnect",
                        "dependencies": [5],
                        "targetCPUID": "D46DC8AB-E25B-AAE8-8B62-F72DD3A4EFC8",
                        "targetDeviceID": "C8993868-AC8D-95D4-6DB4-F1EAE1D61E3F",
                    },
                    {
                        "operationID": 7,
                        "operation": "connect",
                        "dependencies": [],
                        "targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                        "targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                    },
                    {
                        "operationID": 8,
                        "operation": "boot",
                        "dependencies": [7],
                        "targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA",
                    },
                    {
                        "operationID": 9,
                        "operation": "connect",
                        "dependencies": [4, 1],
                        "targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                        "targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                    },
                    {
                        "operationID": 10,
                        "operation": "boot",
                        "dependencies": [9, 2],
                        "targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6",
                    },
                    {
                        "operationID": 11,
                        "operation": "connect",
                        "dependencies": [2, 3],
                        "targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                        "targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                    },
                    {
                        "operationID": 12,
                        "operation": "boot",
                        "dependencies": [11, 4],
                        "targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA",
                    },
                ],
            ),
            (
                {"nodes": []},
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
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
        ],
    )
    def test_plan_system_update_plan_success(self, new, prev, current_list):
        plans = Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))

        assert plans.encode_json() == current_list

    @pytest.mark.parametrize(
        "new,prev",
        [
            ({"nods": []}, {"nodes": []}),  # There is an issue with the node keys.
            ({"nodes": []}, {"noes": []}),  # There is an issue with the node keys.
            ({"node": []}, {"noeds": []}),  # There is an issue with the node keys.
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                            "memory": {
                                "deviceIDs": [
                                    "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                ]
                            },
                        }
                    ]
                },
            ),  # there is no device key
            (
                {
                    "nodes": [
                        {
                            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                            "memory": {
                                "deviceIDs": [
                                    "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                                ]
                            },
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # there is no device key
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": []},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # the deviceIDs value for the CPU is empty
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": []},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # the deviceIDs value for the CPU is empty
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
                {"nodes": [{"device": {}}]},
            ),  # there is a device key, but it is empty
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # the content of the CPU is empty
            (
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                                "storage": {},
                            }
                        }
                    ]
                },
                {
                    "nodes": [
                        {
                            "device": {
                                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # the content of the storage is empty
            (
                {"nodes": []},
                {
                    "nodes": [
                        {
                            "device": {
                                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                            }
                        }
                    ]
                },
            ),  # the content of the cpu is none
        ],
    )
    def test_plan_system_update_plan_failure_when_invalid_input_file(self, new, prev):
        with pytest.raises(Exception):
            Plan.system_update_plan(System.decode_json(prev, {}), System.decode_json(new, {}))
