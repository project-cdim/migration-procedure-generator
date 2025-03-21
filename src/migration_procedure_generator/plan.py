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
"""Migration procedure generation related packages"""

from migration_procedure_generator.operation import Operation


class Task:
    """migration procedure task class"""

    __index_op_id__ = 0

    @classmethod
    def new_op_id(cls):
        """Increment the variable '__index_op_id__'"

        Returns:
            int : operation id
        """
        cls.__index_op_id__ += 1
        return cls.__index_op_id__

    def __init__(self, operation, cpu_id, device_id=None, dependencies=None):
        """constructor

        Args:
            operation (str): Operating Procedures
            cpu_id (str): CPU device ID
            device_id (str, optional): Device ID. Defaults to None.
            dependencies (Task, optional): Task Dependencies. Defaults to None.
        """
        self.op_id = Task.new_op_id()
        self.operation = operation
        self.cpu_id = cpu_id
        self.device_id = device_id
        self.dependencies = dependencies if dependencies else []

    def encode_json(self):
        """Encode the migration procedures in JSON format

        Returns:
            json_data: migration procedure
        """
        json_data = {
            "operationID": self.op_id,
            "operation": self.operation,
            "dependencies": [task.op_id for task in self.dependencies],
        }
        if self.operation != Operation.POWERON and self.operation != Operation.POWEROFF:
            json_data["targetCPUID"] = self.cpu_id
            if self.device_id:
                json_data["targetDeviceID"] = self.device_id
        else:
            json_data["targetDeviceID"] = self.cpu_id
        return json_data

    def get_all_dependencies(self):
        """Get all dependencies associated with a specific Task

        Returns:
            list : dependencies
        """
        return sum([task.get_all_dependencies() for task in self.dependencies], self.dependencies)

    def __eq__(self, other):
        """Comparison method: comparing the input operation ID

        Args:
            other (Task): migration procedures

        Returns:
            bool: true or false
        """
        if other is None or not isinstance(other, Task):
            return False
        return self.op_id == other.op_id

    def __lt__(self, other):
        """Comparison method: comparing the input operation ID

        Args:
            other (Task): migration procedures

        Returns:
            bool: true or false
        """
        return self.op_id < other.op_id


class Plan:
    """migration procedures class"""

    def __init__(self, tasks):
        """constructor

        Args:
            tasks (system): migration procedure
        """
        self.tasks = tasks

    def append(self, task):
        """Add to Task list

        Args:
            task (Task): migration procedure
        """
        self.tasks.append(task)

    def extend(self, other):
        """Add a list to Task list

        Args:
            other (Task): migration procedure
        """
        self.tasks += other.tasks

    def remove(self, task):
        """Remove from the list

        Args:
            task (Task): migration procedure
        """
        self.tasks.remove(task)

    def encode_json(self):
        """Encode the migration procedure into a list type

        Returns:
            list: migration procedure
        """
        return [task.encode_json() for task in self.tasks]

    def device_slice(self, device_id):
        """Retrieve Tasks that have a device ID matching the given ID

        Args:
            device_id (list): Device IDs

        Returns:
            list: migration procedure
        """
        if device_id is None:
            return []
        return [task for task in self.tasks if task.device_id == device_id]

    def cpu_slice(self, cpu_id):
        """Retrieve Tasks that have a CPU device ID matching the given ID

        Args:
            cpu_id (list): CPU Device ID

        Returns:
            list: migration procedure
        """
        return [task for task in self.tasks if task.cpu_id == cpu_id]

    def get_all_cpus(self):
        """Retrieve Tasks that have a cpu_id

        Returns:
            list: CPU device IDs
        """
        return list({task.cpu_id for task in self.tasks})

    def get_all_devices(self):
        """Retrieve Tasks for all devices

        Returns:
            list: device IDs
        """
        return list({task.device_id for task in self.tasks})

    def get_shutdown_tasks(self):
        """Retrieve shutdown tasks

        Returns:
            list: migration procedure
        """
        return {task.cpu_id: task for task in self.tasks if task.operation == Operation.POWEROFF}

    def get_boot_tasks(self):
        """Retrieve boot tasks

        Returns:
            list: migration procedure
        """
        return {task.cpu_id: task for task in self.tasks if task.operation == Operation.POWERON}

    def complete_device_dependencies(self):
        """Organize dependencies"""
        self.tasks.sort()
        self.create_device_dependencies()
        self.create_shutdown_dependencies()
        self.create_boot_dependencies()

    def create_device_dependencies(self):
        """create connect and disconnect task dependencies"""
        for device_id in self.get_all_devices():
            device_slice = self.device_slice(device_id)
            # Verifying from the next task, as the 0th element contains the same task.
            for depended, depending in zip(device_slice, device_slice[1:]):
                depending.dependencies.append(depended)

    def create_shutdown_dependencies(self):
        """create shutdown task dependencies"""
        shutdown_tasks = self.get_shutdown_tasks()
        for task in self.tasks:
            if task.operation == Operation.CONNECT and task.cpu_id in shutdown_tasks:
                shutdown_task = shutdown_tasks[task.cpu_id]
                if shutdown_task not in task.dependencies:
                    task.dependencies.append(shutdown_task)

    def create_boot_dependencies(self):
        """create boot task dependencies"""
        boot_tasks = self.get_boot_tasks()
        for task in self.tasks:
            if task.operation == Operation.DISCONNECT and task.cpu_id in boot_tasks:
                boot_task = boot_tasks[task.cpu_id]
                if task not in boot_task.dependencies:
                    boot_task.dependencies.append(task)

    @classmethod
    def system_update_plan(cls, prev, new):
        """Create migration procedure

        Args:
            prev (task): current Layout
            new (task): desired Layout

        Returns:
            plan: migration procedures
        """
        plan = Plan.system_destruct_plan(prev)
        new_construct_plan = Plan.system_construct_plan(new)
        plan.extend(new_construct_plan)
        plan.remove_redundant_tasks()
        plan.complete_device_dependencies()
        plan.remove_indirect_dependencies()
        return plan

    def remove_redundant_tasks(self):
        """Remove redundant migration procedure"""
        self.tasks.sort()
        for device_id in self.get_all_devices():
            device_slice = self.device_slice(device_id)
            # Verifying whether the operations on the same device are limited to two (connect and disconnect only).
            if len(device_slice) == 2 and device_slice[0].cpu_id == device_slice[1].cpu_id:
                self.remove(device_slice[0])
                self.remove(device_slice[1])
        for cpu_id in self.get_all_cpus():
            cpu_slice = self.cpu_slice(cpu_id)
            # Verifying whether the operations on the CPU are limited to two (boot and shutdown only).
            if len(cpu_slice) == 2 and cpu_slice[0].device_id is None and cpu_slice[1].device_id is None:
                self.remove(cpu_slice[0])
                self.remove(cpu_slice[1])
        self.remove_invalid_dependencies()

    def remove_invalid_dependencies(self):
        """Remove tasks that are invalid from dependencies"""
        self.tasks.sort()
        task_ids = {task.op_id for task in self.tasks}
        for task in self.tasks:
            task.dependencies = [depending for depending in task.dependencies if depending.op_id in task_ids]

    def remove_indirect_dependencies(self):
        """Remove tasks with an indirect status from dependencies"""
        self.tasks.sort()
        for task in reversed(self.tasks):
            for depending in task.dependencies.copy():
                for ind_depending in depending.get_all_dependencies():
                    if ind_depending in task.dependencies:
                        task.dependencies.remove(ind_depending)

    @classmethod
    def system_destruct_plan(cls, system):
        """Create destructive migration procedure

        Args:
            system (system): Create a node for stop and disconnect procedures.

        Returns:
            plan: migration procedures
        """
        plan = Plan([])
        for node in system.nodes:
            plan.extend(Plan.node_destruct_plan(node))
        return plan

    @classmethod
    def node_destruct_plan(cls, node):
        """Create destructive task

        Args:
            node (system): Create a node for stop and disconnect procedures.

        Returns:
            plan: migration procedures
        """
        plan = Plan([])
        task_sd = Task(Operation.POWEROFF, node.cpu)
        plan.append(task_sd)
        for device_id in node.other_devices:
            task_disconnect = Task(Operation.DISCONNECT, node.cpu, device_id, [task_sd])
            plan.append(task_disconnect)
        return plan

    @classmethod
    def system_construct_plan(cls, system):
        """Create constructive migration procedures

        Args:
            system (system): system to create boot and connection procedures

        Returns:
            plan: migration procedures
        """
        plan = Plan([])
        for node in system.nodes:
            plan.extend(Plan.node_construct_plan(node))
        return plan

    @classmethod
    def node_construct_plan(cls, node):
        """Create constructive task

        Args:
            node (system): Node to create boot and connection procedures

        Returns:
            plan: migration procedures
        """
        plan = Plan([])
        for device_id in node.other_devices:
            task_connect = Task(Operation.CONNECT, node.cpu, device_id, [])
            plan.append(task_connect)
        task_bt = Task(Operation.POWERON, node.cpu, dependencies=plan.tasks.copy())
        plan.append(task_bt)
        return plan
