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


class Node:
    """Node class: storing CPU and other device properties at the node level"""

    def __init__(self, devices, bound_devices_map):
        """constructor

        Args:
            devices (dict): layout
        """
        # The program, originally provided by Research Institute,
        # but it is currently commented out as it is not being used.
        # self.services = services
        self.devices = devices
        self.filtering_devices(bound_devices_map)

    @property
    def cpu(self):
        """Get cpu device id

        Returns:
            str: CPU device ID
        """
        # The current migration process does not consider MLD (Multi-Link for Derived Transport),
        # therefore it only refers to the CPU at the beginning.
        return self.devices["cpu"]["deviceIDs"][0]

    @property
    def other_devices(self):
        """Get device ids

        Returns:
            list : device IDs
        """
        all_device_ids = []
        for device_type, device_def in self.devices.items():
            device_ids = device_def["deviceIDs"]
            if device_type != "cpu":
                all_device_ids.extend(device_ids)
        return all_device_ids

    @classmethod
    def decode_json(cls, json_data, bound_devices_map):
        """Conversion of Json types to node class

        Args:
            json_data (dict): layout

        Returns:
            Node: layout
        """
        # The program, originally provided by Research Institute,
        # but it is currently commented out as it is not being used.
        # return Node(json_data["services"], json_data["device"], bound_devices_map)
        return Node(json_data["device"], bound_devices_map)

    def filtering_devices(self, bound_devices_map):
        """Filter the device

        Args:
            bound_devices_map (dict): bound devices map
        """
        bound_devices = bound_devices_map.get(self.cpu, {})
        for device_type in self.devices.keys():
            self.devices[device_type]["deviceIDs"] = [
                device_id
                for device_id in self.devices[device_type]["deviceIDs"]
                if device_id not in bound_devices.get(device_type, [])
            ]


class System:
    """System class: storing data in Node class objects at the node level"""

    def __init__(self, nodes):
        """constructor

        Args:
            nodes (Node): layout
        """
        self.nodes = nodes

    @classmethod
    def decode_json(cls, json_data, bound_devices_map):
        """Conversion of node class to system class

        Args:
            json_data (dict): layout

        Returns:
            system: layout
        """
        nodes = [Node.decode_json(node, bound_devices_map) for node in json_data["nodes"]]
        return System(nodes)
