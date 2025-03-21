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
import logging

import pytest

from migration_procedure_generator.setting import MigrationConfigReader, initialize_log
from migration_procedure_generator.cdimlogger import Logger


class TestMigrationConfigReader:
    def test_success_read_configuration_file_and_interpret_settings(self):
        obj = MigrationConfigReader()
        assert isinstance(obj.log_config, dict)
        assert isinstance(obj.migration_procedures_config, dict)

    @pytest.mark.parametrize(
        "update_confg",
        [
            # host value is correctly
            {
                "migration_procedures": {
                    "host": "0.0.0.0",
                    "port": 8003,
                },
            },
            # host value is correctly
            {
                "migration_procedures": {
                    "host": "nec.test.com",
                    "port": 8003,
                },
            },
            # port value is correctly
            {
                "migration_procedures": {
                    "host": "nec.test.com",
                    "port": 0,
                },
            },
        ],
    )
    def test_success_without_validation_error_from_migration_procedures_settings(self, mocker, update_confg):

        base_config = {
            "log": {
                "logging_level": "INFO",
                "log_dir": "./",
                "file": "app_migration_procedures.log",
                "rotation_size": 1000000,
                "backup_files": 3,
                "stdout": False,
            },
        }
        config = {**base_config, **update_confg}
        mocker.patch("yaml.safe_load").return_value = config
        server = MigrationConfigReader().migration_procedures_config
        assert server == update_confg.get("migration_procedures")

    @pytest.mark.parametrize(
        "update_confg",
        [
            # logging_level:INFO
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {  # logging_level:ERROR
                "log": {
                    "logging_level": "ERROR",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {  # logging_level:WARN
                "log": {
                    "logging_level": "WARN",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {  # logging_level:CRITICAL
                "log": {
                    "logging_level": "CRITICAL",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {  # logging_level:DEBUG
                "log": {
                    "logging_level": "DEBUG",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # # logging_level is None
            {
                "log": {
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # log_dir:./
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # log_dir is None
            {
                "log": {
                    "logging_level": "INFO",
                    "file": "app_migration_procedures.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # file:a
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "file": "a",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # file is none
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # rotation_size:int
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "file": "a",
                    "rotation_size": 0,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # rotation_size is None
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # backup_files:int
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "file": "a",
                    "rotation_size": 0,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            # backup_files is None
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "rotation_size": 1000000,
                    "stdout": False,
                }
            },
            # stdout:False
            {
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {  # stdout:True
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": True,
                }
            },
            {  # stdout is None
                "log": {
                    "logging_level": "INFO",
                    "log_dir": "./",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                }
            },
            # param is None
            {},
        ],
    )
    def test_success_without_validation_error_from_logging_settings(self, mocker, update_confg):

        base_config = {
            "log": {
                "logging_level": "INFO",
                "log_dir": "./",
                "file": "app_migration_procedures.log",
                "rotation_size": 1000000,
                "backup_files": 3,
                "stdout": False,
            },
            "migration_procedures": {
                "host": "0.0.0.0",
                "port": 8010,
            },
        }
        config = {**base_config, **update_confg}
        mocker.patch("yaml.safe_load").return_value = config
        MigrationConfigReader().log_config

    def test_log_config_failure_when_file_not_found_error(self, mocker):
        config = {
            "log": {
                "logging_level": "INFO",
                "log_dir": "/lllllll/log/nec/gi",
                "file": "app_migration_procedures.log",
                "rotation_size": 1000000,
                "backup_files": 3,
                "stdout": False,
            },
            "migration_procedures": {
                "host": "0.0.0.0",
                "port": 8010,
            },
        }
        mocker.patch("yaml.safe_load").return_value = config
        with pytest.raises(Exception):
            MigrationConfigReader().log_config


class TestLogger:
    @pytest.mark.parametrize(
        "log_level",
        [
            (
                {
                    "log": {
                        "logging_level": "DEBUG",
                        "log_dir": "./",
                        "file": "app_migration_procedures.log",
                        "rotation_size": 1000000,
                        "backup_files": 3,
                        "stdout": False,
                    },
                    "migration_procedures": {
                        "host": "localhost",
                        "port": 8010,
                    },
                }
            ),  # log level:DEBUG
            (
                {
                    "log": {
                        "logging_level": "WARN",
                        "log_dir": "./",
                        "file": "app_migration_procedures.log",
                        "rotation_size": 1000000,
                        "backup_files": 3,
                        "stdout": False,
                    },
                    "migration_procedures": {
                        "host": "localhost",
                        "port": 8010,
                    },
                }
            ),  # log level:WARN
            (
                {
                    "log": {
                        "logging_level": "ERROR",
                        "log_dir": "./",
                        "file": "app_migration_procedures.log",
                        "rotation_size": 1000000,
                        "backup_files": 3,
                        "stdout": False,
                    },
                    "migration_procedures": {
                        "host": "localhost",
                        "port": 8010,
                    },
                }
            ),  # log level:ERROR
            (
                {
                    "log": {
                        "logging_level": "CRITICAL",
                        "log_dir": "./",
                        "file": "app_migration_procedures.log",
                        "rotation_size": 1000000,
                        "backup_files": 3,
                        "stdout": False,
                    },
                    "migration_procedures": {
                        "host": "localhost",
                        "port": 8010,
                    },
                }
            ),  # log level:CRITICAL
            (
                {
                    "log": {
                        "logging_level": "INFO",
                        "log_dir": "./",
                        "file": "app_migration_procedures.log",
                        "rotation_size": 1000000,
                        "backup_files": 3,
                        "stdout": False,
                    },
                    "migration_procedures": {
                        "host": "localhost",
                        "port": 8010,
                    },
                }
            ),  # log level:INFO
        ],
    )
    def test_logger_success_log_level_from_configuration_file(self, mocker, log_level):
        mocker.patch("yaml.safe_load").return_value = log_level
        glogger: Logger = initialize_log()
        log_level_str = logging.getLevelName(glogger.logger.getEffectiveLevel())
        log_level_str = "WARN" if log_level_str == "WARNING" else log_level_str
        assert log_level_str == log_level["log"]["logging_level"]
