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
import os
import sys
import tempfile
import uuid

import pytest
import yaml

from migration_procedure_generator.core import ExitCode, main
from migration_procedure_generator.plan import Task
from migration_procedure_generator.setting import MigrationConfigReader, MigrationLogConfigReader
from migration_procedure_generator.custom_exception import SettingFileValidationError

@pytest.fixture(scope="function", autouse=True)
def initializetask():
    # Initialize so that the test for other things doesn't affect it
    Task.__index_op_id__ = 0


@pytest.fixture
def get_tmp_twoNode_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
        "nodes": [
            {
                "device": {
                    "cpu": {"deviceIDs": ["ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"]},
                    "memory": {
                        "deviceIDs": [
                            "5DFB4893-C16D-4968-89D6-8D1EAECEA31F",
                        ]
                    },
                    "storage": {"deviceIDs": ["2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"]},
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
    }

    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


@pytest.fixture
def get_tmp_oneNode_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
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
        ]
    }
    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


@pytest.fixture
def get_tmp_Empty_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {"nodes": []}
    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


@pytest.fixture
def get_tmp_varidation_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
        "nodes": [
            {
                "device": {
                    "CpU": {"deviceIDs": ["6c58b2c0-70a9-4a67-a04c-7d249dff5a96"]},
                }
            },
            {
                "device": {
                    "CPU": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                    "Memory": {
                        "deviceIDs": [
                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                        ]
                    },
                    "storagE": {
                        "deviceIDs": [
                            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                        ]
                    },
                    "NeTwOrKiNtErFaCe": {"deviceIDs": []},
                    "gPu": {"deviceIDs": []},
                }
            },
        ]
    }
    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


@pytest.fixture
def get_boundDecices_varidation_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
        "nodes": [
            {
                "device": {
                    "CPU": {"deviceIDs": ["3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"]},
                    "Memory": {
                        "deviceIDs": [
                            "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F",
                        ]
                    },
                    "storagE": {
                        "deviceIDs": [
                            "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15",
                        ]
                    },
                    "NeTwOrKiNtErFaCe": {"deviceIDs": []},
                    "gPu": {"deviceIDs": []},
                }
            },
        ],
        "boundDevices": {
            "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA": {
                "mEmOrY": ["388e64e3-efa7-484c-b63c-28bf1709d6c1"],
                "StOrAgE": ["33f19666-68b3-4ed7-a9a8-d046f0879ff2"],
                "GpU": ["06ebec09-553a-462e-96f9-f58909180428"],
                "nEtWoRkInTeRfAcE": ["8d45fffa-e7f5-462f-88d3-94ef9b46a8ab"],
            }
        },
    }
    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


@pytest.fixture
def get_tmp_yaml_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
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
        ]
    }
    with tempfile.TemporaryDirectory() as dir_path:
        yaml_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.yaml")
        with open(yaml_file, mode="w", encoding="utf-8") as fh:
            yaml.safe_dump(
                json_data,
                fh,
                indent=2,
                allow_unicode=True,
                sort_keys=False,
                explicit_start=True,
                encoding="utf-8",
            )
        try:
            yield yaml_file
        finally:
            os.remove(yaml_file)


@pytest.fixture
def get_tmp_value_error_json_file():
    """A test temporary file is created for the purpose of testing and evaluation."""
    json_data = {
        "node": [
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
        ]
    }
    with tempfile.TemporaryDirectory() as dir_path:
        json_file = os.path.join(dir_path, f"{str(uuid.uuid4())}.json")
        with open(json_file, mode="w", encoding="utf-8") as fh:
            json.dump(json_data, fh, indent=4)
        try:
            yield json_file
        finally:
            os.remove(json_file)


class TestMain:
    @pytest.mark.parametrize("args", [(["-h"]), (["--help"])])
    def test_main_success_when_display_help_Message(self, args, capfd):
        sys.argv = ["core.py", *args]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == 0
        out, _ = capfd.readouterr()
        assert "usage" in out
        assert "options:" in out
        assert "-h" in out
        assert "--help" in out
        assert "--prev" in out
        assert "DESIRED_LAYOUT_FILE" in out
        assert "--new" in out
        assert "CURRENT_LAYOUT_FILE" in out
        # Check for ite.14 fix(will be deleted later)
        assert "BEFORE_LAYOUT_FILE" not in out
        assert "AFTER_LAYOUT_FILE" not in out

    def test_main_success(self, capfd, get_tmp_oneNode_json_file, get_tmp_twoNode_json_file):
        sys.argv = ["core.py", "--prev", get_tmp_oneNode_json_file, "--new", get_tmp_twoNode_json_file]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()

        assert '"operationID": 1' in out
        assert '"operation": "shutdown"' in out
        assert '"dependencies": []' in out
        assert '"targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"' in out

        assert '"operationID": 2' in out
        assert '"operation": "disconnect"' in out
        assert '"dependencies": [1]' in out
        assert '"targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"' in out
        assert '"targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"' in out

        assert '"operationID": 3' in out
        assert '"operation": "connect"' in out
        assert '"dependencies": []' in out
        assert '"targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"' in out
        assert '"targetDeviceID": "5DFB4893-C16D-4968-89D6-8D1EAECEA31F"' in out

        assert '"operationID": 4' in out
        assert '"operation": "connect"' in out
        assert '"dependencies": []' in out
        assert '"targetCPUID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"' in out
        assert '"targetDeviceID": "2CA6D4DF-2739-45BA-ACA4-6ABE93E81E15"' in out

        assert '"operationID": 5' in out
        assert '"operation": "boot"' in out
        assert '"dependencies": [3, 4]' in out
        assert '"targetDeviceID": "ABA3E4EB-8C5B-E46D-8D62-C272DD8AF8FA"' in out

        assert '"operationID": 6' in out
        assert '"operation": "connect"' in out
        assert '"dependencies": [2]' in out
        assert '"targetCPUID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"' in out
        assert '"targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"' in out

        assert '"operationID": 7' in out
        assert '"operation": "boot"' in out
        assert '"dependencies": [6]' in out
        assert '"targetDeviceID": "EBA3E4EB-5BDD-46DA-8C8A-272F8D62C8FA"' in out

    def test_main_success_when_prev_is_empty(self, capfd, get_tmp_oneNode_json_file, get_tmp_Empty_json_file):
        sys.argv = ["core.py", "--prev", get_tmp_Empty_json_file, "--new", get_tmp_oneNode_json_file]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()

        assert '"operationID": 1' in out
        assert '"operation": "connect"' in out
        assert '"dependencies": []' in out
        assert '"targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"' in out
        assert '"targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"' in out
        assert '"operationID": 2' in out
        assert '"operation": "boot"' in out
        assert '"dependencies": [1]' in out
        assert '"targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"}' in out

    def test_main_success_when_new_is_empty(self, capfd, get_tmp_oneNode_json_file, get_tmp_Empty_json_file):
        sys.argv = ["core.py", "--prev", get_tmp_oneNode_json_file, "--new", get_tmp_Empty_json_file]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()
        assert '"operationID": 1' in out
        assert '"operation": "shutdown"' in out
        assert '"dependencies": []' in out
        assert '"targetDeviceID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"' in out
        assert '"operationID": 2' in out
        assert '"operation": "disconnect"' in out
        assert '"dependencies": [1]' in out
        assert '"targetCPUID": "3B4EBEEA-B6DD-45DA-8C8A-2CA2F8F728D6"' in out
        assert '"targetDeviceID": "895DFB43-68CD-41D6-8996-EAC8D1EA1E3F"' in out

    def test_main_success_when_prev_and_new_is_empty(self, capfd, get_tmp_Empty_json_file):
        sys.argv = ["core.py", "--prev", get_tmp_Empty_json_file, "--new", get_tmp_Empty_json_file]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()
        assert "[]\n" == out

    @pytest.mark.parametrize(
        "args",
        [
            (["--prev", "error", "--new", "correct"]),
            (["--prev", "correct", "--new", "error"]),
            (["--prev", "error", "--new", "error"]),
        ],
    )
    def test_main_failure_when_varidation_error_is_detected(
        self, args, capfd, get_tmp_oneNode_json_file, get_tmp_value_error_json_file
    ):
        for element in args:
            if element == "correct":
                args[args.index(element)] = get_tmp_oneNode_json_file
            if element == "error":
                args[args.index(element)] = get_tmp_value_error_json_file
        sys.argv = ["core.py", *args]

        with pytest.raises(SystemExit) as excinfo:
            main()
        _, err = capfd.readouterr()
        assert excinfo.value.code == ExitCode.VALIDATION_ERROR
        assert "[E50001]'nodes' is a required property" in err

    @pytest.mark.parametrize(
        "args", [(["--prev", "update"]), (["--new", "update"]), ([])]  # prev only  # new only  # no parameter
    )
    def test_main_failure_when_parameter_is_not_specified(self, args, capfd, get_tmp_oneNode_json_file):
        for element in args:
            if element == "update":
                args[args.index(element)] = get_tmp_oneNode_json_file
        sys.argv = ["core.py", *args]

        with pytest.raises(SystemExit):
            main()
        _, err = capfd.readouterr()
        assert "usage" in err
        assert "[-h]" in err
        assert "--prev CURRENT_LAYOUT_FILE" in err
        assert "--new DESIRED_LAYOUT_FILE" in err

    @pytest.mark.parametrize(
        "args",
        [
            (["--prev", "update", "--new", "/var/log/nec/gi/tmp_file.json"]),  # prev only
            (["--prev", "/var/log/nec/gi/tmp_file.json", "--new", "update"]),  # prev only
            (["--prev", "/var/log/nec/gi/tmp_file.json", "--new", "/var/log/nec/gi/tmp_file.json"]),  # prev and new
        ],
    )
    def test_main_failure_when_specified_file_not_found(self, args, capfd, get_tmp_oneNode_json_file):
        for element in args:
            if element == "update":
                args[args.index(element)] = get_tmp_oneNode_json_file

        sys.argv = ["core.py", *args]

        with pytest.raises(SystemExit) as excinfo:
            main()
        _, err = capfd.readouterr()
        assert excinfo.value.code == ExitCode.VALIDATION_ERROR
        assert "[E50001]Specified file not found:" in err

    @pytest.mark.parametrize(
        "args",
        [
            (["--prev", "update", "--new", "correct"]),  # prev only
            (["--prev", "correct", "--new", "update"]),  # prev only
            (["--prev", "update", "--new", "update"]),  # prev and new
        ],
    )
    def test_main_failure_when_file_json_decode_error(self, args, capfd, get_tmp_oneNode_json_file, get_tmp_yaml_file):
        for element in args:
            if element == "update":
                args[args.index(element)] = get_tmp_yaml_file
            elif element == "correct":
                args[args.index(element)] = get_tmp_oneNode_json_file
        sys.argv = ["core.py", *args]

        with pytest.raises(SystemExit) as excinfo:
            main()
        _, err = capfd.readouterr()
        assert excinfo.value.code == ExitCode.VALIDATION_ERROR
        assert "[E50001]Specified file not in JSON format" in err

    @pytest.mark.parametrize(
        "args",
        [
            (["--prev", "update", "--new", "correct"]),  # prev only
            (["--prev", "correct", "--new", "update"]),  # prev only
            (["--prev", "update", "--new", "update"]),  # prev and new
        ],
    )
    def test_main_failure_when_file_load_exception(
        self, args, capfd, mocker, get_tmp_oneNode_json_file, get_tmp_yaml_file
    ):
        for element in args:
            if element == "update":
                args[args.index(element)] = get_tmp_yaml_file
            elif element == "correct":
                args[args.index(element)] = get_tmp_oneNode_json_file
        sys.argv = ["core.py", *args]
        mocker.patch("json.load", side_effect=[Exception("File has no permission")])

        with pytest.raises(SystemExit) as excinfo:
            main()
        _, err = capfd.readouterr()
        assert excinfo.value.code == ExitCode.VALIDATION_ERROR
        assert "[E50001]Specified file can not open:" in err

    def test_main_failure_when_initialize_log_error(self, mocker, capfd, get_tmp_oneNode_json_file):
        """abnormal system testing"""
        sys.argv = ["core.py", "--prev", get_tmp_oneNode_json_file, "--new", get_tmp_oneNode_json_file]
        mocker.patch("yaml.safe_load", side_effect=[FileNotFoundError("file is not exsist")])

        with pytest.raises(SystemExit) as excinfo:
            main()
        _, err = capfd.readouterr()
        assert excinfo.value.code == 2
        assert "[E50005]Failed to load migrationprocedures_log_config.yaml\n" in err

    def test_main_failed_when_log_initialization_error(
        self, mocker, capfd, get_tmp_oneNode_json_file, get_tmp_Empty_json_file
    ):
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
                                'filename': '/var/log/midc/app_migration_procedures.log',
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
        sys.argv = ["core.py", "--prev", get_tmp_oneNode_json_file, "--new", get_tmp_Empty_json_file]
        with pytest.raises(SystemExit) as e:
            main()
        _, err = capfd.readouterr()
        assert e.value.code == 3
        assert "[E50006]Internal server error. Failed in log initialization.\n" in err

    def test_main_success_when_key_name_are_case_insensitive(self, capfd, get_tmp_varidation_json_file):
        sys.argv = ["core.py", "--prev", get_tmp_varidation_json_file, "--new", get_tmp_varidation_json_file]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()
        assert "[]\n" == out

    def test_main_success_when_key_name_are_case_insensitive_boundDevices(
        self, capfd, get_boundDecices_varidation_json_file
    ):
        sys.argv = [
            "core.py",
            "--prev",
            get_boundDecices_varidation_json_file,
            "--new",
            get_boundDecices_varidation_json_file,
        ]
        with pytest.raises(SystemExit) as excinfo:
            main()
        assert excinfo.value.code == ExitCode.NORMAL
        out, _ = capfd.readouterr()
        assert "[]\n" == out
