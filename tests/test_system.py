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

from migration_procedure_generator.system import Node, System


class TestNode:

    def test_success_cpu_get_infomation(self):
        node_json = {
            "device": {
                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                "memory": {
                    "deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]
                },
                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
            }
        }

        node = Node.decode_json(node_json, {})
        assert node.cpu == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"

    def test_node_success_devices_get_infomation(self):
        """Normal-case testing: device information only"""
        node_json = {
            "device": {
                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                "memory": {
                    "deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]
                },
                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
            }
        }

        node = Node.decode_json(node_json, {})

        assert node.devices == {
            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
            "memory": {"deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]},
            "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
            "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
        }

    def test_node_success_other_devices_get_information(self):
        """Normal-case testing: device information only"""
        node_json = {
            "device": {
                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                "memory": {
                    "deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]
                },
                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
            }
        }

        node = Node.decode_json(node_json, {})
        assert node.other_devices == [
            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
            "AACA46AB-E92C-A6D4-DF27-3945B3E81E15",
        ]

    def test_node_success_device_information_when_added_service(self):
        """Normal-case testing: device information and service information."""
        node_json = {
            "services": [{"id": "sv#1", "requestInstanceID": "1"}],
            "device": {
                "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                "memory": {
                    "deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]
                },
                "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
            },
        }

        node = Node.decode_json(node_json, {})

        assert node.cpu == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert node.devices == {
            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
            "memory": {"deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]},
            "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
            "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
        }
        assert node.other_devices == [
            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
            "AACA46AB-E92C-A6D4-DF27-3945B3E81E15",
        ]


class TestSystem:
    def test_system_success_node_information(self):
        """Normal-case testing: device information only"""
        node = {
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
                        "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                        "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
                    }
                }
            ]
        }

        decode_json = System.decode_json(node, {})
        assert decode_json.nodes[0].cpu == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert decode_json.nodes[0].devices == {
            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
            "memory": {"deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]},
            "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
            "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
        }
        assert decode_json.nodes[0].other_devices == [
            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
            "AACA46AB-E92C-A6D4-DF27-3945B3E81E15",
        ]

    def test_system_success_nodeinformation_when_added_service(self):
        """Normal-case testing: device information and service information."""
        node = {
            "nodes": [
                {
                    "services": [{"id": "sv#1", "requestInstanceID": "1"}],
                    "device": {
                        "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                        "memory": {
                            "deviceIDs": [
                                "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                                "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                            ]
                        },
                        "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
                        "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
                    },
                }
            ]
        }

        decode_json = System.decode_json(node, {})
        assert decode_json.nodes[0].cpu == "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"
        assert decode_json.nodes[0].devices == {
            "cpu": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
            "memory": {"deviceIDs": ["895DFB43-68CD-41D6-8996-EAC8D1EA1E3F", "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"]},
            "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
            "networkInterface": {"deviceIDs": ["AACA46AB-E92C-A6D4-DF27-3945B3E81E15"]},
        }
        assert decode_json.nodes[0].other_devices == [
            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
            "AACA46AB-E92C-A6D4-DF27-3945B3E81E15",
        ]

    def test_system_when_system_is_empty(self):
        nodes = {"nodes": []}
        decode_json = System.decode_json(nodes, {})
        assert decode_json.nodes == []

    @pytest.mark.parametrize(
        "nodes",
        [
            ({"nods": []}),  # There is an issue with the node keys.
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
                }
            ),  # there is no device key
        ],
    )
    def test_system_failure_check_error_pattern(self, nodes):
        with pytest.raises(Exception):
            System.decode_json(nodes, {})
