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

from migration_procedure_generator.custom_exception import (
    LogInitializationError,
    SettingFileValidationError,
    LogSettingFileValidationError,
)
from migration_procedure_generator.schema import config_schema, log_config_schema
from migration_procedure_generator.common.logger import Logger


class MigrationLogConfigReader(BaseConfig):
    """A class to read logging configuration files"""
    def __init__(self):
        """constructor"""
        try:
            super().__init__("migration_procedure_generator.config", "migrationprocedures_log_config.yaml")
            validate(self._config, log_config_schema)
            filename = self._config.get("handlers", {}).get("file", {}).get("filename")
            log_dir = os.path.dirname(filename)
            self._check_directory_exists(log_dir)
        except Exception as error:
            raise LogSettingFileValidationError(error.args) from error

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
        return self._config


class MigrationConfigReader(BaseConfig):
    """A class to read configuration files"""

    def __init__(self) -> None:
        """constructor"""
        try:
            super().__init__("migration_procedure_generator.config", "migrationprocedures_config.yaml")
            validate(self._config, config_schema)

        except Exception as error:
            raise SettingFileValidationError(error.args) from error

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
    log_config = MigrationLogConfigReader().log_config

    try:
        logger = Logger(log_config)
    except Exception as err:
        raise LogInitializationError() from err
    return logger
