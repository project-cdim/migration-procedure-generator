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
"""Common module"""

import os

from jsonschema import validate
from migration_procedure_generator.common.config import BaseConfig

from migration_procedure_generator.cdimlogger import Logger
from migration_procedure_generator.cdimlogger.common import CRITICAL, DEBUG, ERROR, INFO, TAG_APP_POLICY, WARN
from migration_procedure_generator.custom_exception import LogInitializationError, SettingFileValidationError
from migration_procedure_generator.schema import config_schema


class MigrationConfigReader(BaseConfig):
    """A class to read configuration files"""

    def __init__(self) -> None:
        """constructor"""
        try:
            super().__init__("migration_procedure_generator.config", "migrationprocedures_config.yaml")

            log_dir = self.log_config.get("log_dir", None)
            if log_dir:
                self._check_directory_exists(log_dir)
            validate(self._config, config_schema)
        except Exception as error:
            raise SettingFileValidationError(error.args) from error

    def _check_directory_exists(self, path: str) -> None:
        """Checking if a directory exists

        Args:
            path (str): directory path

        Raises:
            FileNotFoundError: file not found
        """
        if not os.path.isdir(path):
            raise FileNotFoundError(f"Directory not found at path: {path}")

    @property
    def log_config(self) -> dict:
        """Reading log configuration data from an migration procedure generator settings file

        Returns:
            dict: read config date
        """
        return self._config.get("log")

    @property
    def migration_procedures_config(self) -> dict:
        """Reading server settings from a migration procedure configuration file

        Returns:
            dict: read config date
        """
        return self._config.get("migration_procedures")


def initialize_log() -> Logger:
    """Logger Object return

    Returns:
        Logger: Logger Object
    """
    log_config = MigrationConfigReader().log_config

    match log_config.get("logging_level", INFO).upper():
        case "DEBUG":
            LOGGING_LVL = DEBUG  # pylint: disable=C0103
        case "WARN":
            LOGGING_LVL = WARN  # pylint: disable=C0103
        case "ERROR":
            LOGGING_LVL = ERROR  # pylint: disable=C0103
        case "CRITICAL":
            LOGGING_LVL = CRITICAL  # pylint: disable=C0103
        case _:
            LOGGING_LVL = INFO  # pylint: disable=C0103

    try:
        logger = Logger(
            tag=TAG_APP_POLICY,
            log_dir=log_config.get("log_dir", ""),
            log_file=log_config.get("file", ""),
            logging_level=LOGGING_LVL,
            stdout=log_config.get("stdout", ""),
            rotation_size=log_config.get("rotation_size", ""),
            backup_files=log_config.get("backup_files", False),
        )
    except Exception as err:
        raise LogInitializationError() from err
    return logger
