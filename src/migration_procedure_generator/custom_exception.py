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
"""Custom Exception Package"""

import sys
from abc import abstractmethod

from fastapi.exceptions import RequestValidationError

from migration_procedure_generator.exitcode import ExitCode


class CustomBaseException(Exception):
    """Base Exception class"""

    @abstractmethod
    def output_stderr(self) -> None:
        """Print messages for CLI"""

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""


class SettingFileValidationError(CustomBaseException):
    """Configuration File Error Class"""

    def __init__(self, message):
        """constructor

        Args:
            message (str): Location of error occurrence
        """
        super().__init__(message)
        self.message = f"Failed to load migrationprocedures_config.yaml\n{message}"

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50005]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.CONFIG_ERROR

    @property
    def response_msg(self) -> dict:
        """Return a response message"""
        return {"code": "E50005", "message": self.message}


class JSONDecodeError(CustomBaseException):
    """Json decode error class"""

    def __init__(self):
        """constructor"""
        super().__init__()
        self.message = "Specified file not in JSON format"

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50001]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.VALIDATION_ERROR


class NotFoundError(CustomBaseException):
    """File not found Error class"""

    def __init__(self, file_path):
        """constructor

        Args:
            file_path (str): error file path
        """
        super().__init__(file_path)
        self.message = f"Specified file not found: {file_path}"

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50001]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.VALIDATION_ERROR


class FileReadError(CustomBaseException):
    """File loading Error Class"""

    def __init__(self, file_path):
        """constructor

        Args:
            file_path (str): error file path
        """
        super().__init__(file_path)
        self.message = f"Specified file can not open: {file_path}"

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50001]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.VALIDATION_ERROR


class JsonSchemaError(CustomBaseException):
    """Jsonschema error class"""

    def __init__(self, message):
        """constructor

        Args:
            message (str): Location of error occurrence
        """
        super().__init__(message)
        self.message = message

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50001]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.VALIDATION_ERROR

    @property
    def response_msg(self) -> dict:
        """Return a response message"""
        return {"code": "E50001", "message": self.message}


class RequestError:
    """Request Error Class"""

    def __init__(self, exc: RequestValidationError):
        """constructor

        Args:
            exc (RequestValidationError): Request validation error occurred.
        """
        self.message = exc.errors()

    @property
    def response_msg(self) -> dict:
        """Return a response message"""
        return {"code": "E50001", "message": self.message}


class LogInitializationError(CustomBaseException):
    """Log initialization error class"""

    def __init__(self):
        """constructor"""
        super().__init__()
        self.message = "Internal server error. Failed in log initialization."

    def output_stderr(self) -> None:
        """Print messages for CLI"""
        print(f"[E50006]{self.message}", file=sys.stderr)

    @property
    def exit_code(self) -> int:
        """Retrieve ExitCode"""
        return ExitCode.INTERNAL_ERR

    @property
    def response_msg(self) -> dict:
        """Return a response message"""
        return {"code": "E50006", "message": self.message}
