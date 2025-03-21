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
"""migration procedure generator restapi"""

from http import HTTPStatus

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from migration_procedure_generator.custom_exception import (
    CustomBaseException,
    JsonSchemaError,
    RequestError,
    SettingFileValidationError,
    LogInitializationError,
)
from migration_procedure_generator.model import NodeLayout
from migration_procedure_generator.plan import Plan, Task
from migration_procedure_generator.setting import MigrationConfigReader, initialize_log
from migration_procedure_generator.system import System

app = FastAPI()
BASEURL = "/cdim/api/v1/"


# Avoid CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Setting up to allow responses
    # Setting up to allow credentials
    # (cookies, authentication headers, client certificates) in CORS requests
    allow_credentials=True,
    allow_methods=["*"],  # Setting up to allow request methods in CORS requests
    allow_headers=["*"],  # Setting up to allow headers in CORS requests
)


@app.exception_handler(RequestValidationError)
def validate_request_handler(_, exc: RequestValidationError):
    """Custom Error Handler. If a validation error occurs when using Pydantic"""

    request_error = RequestError(exc)
    return JSONResponse(
        content=request_error.response_msg,
        status_code=HTTPStatus.BAD_REQUEST.value,
    )


@app.exception_handler(JsonSchemaError)
def jsonschema_validation_handler(_, exc: JsonSchemaError):
    """Custom Error Handler. To handle validation errors
    that occur when validating against a JsonSchema, and return a response
    """
    return JSONResponse(
        content=exc.response_msg,
        status_code=HTTPStatus.BAD_REQUEST.value,
    )


@app.exception_handler(SettingFileValidationError)
def setting_validation_handler(_, exc: SettingFileValidationError):
    """Return an error code and message if an error occurs in the configuration file."""
    return JSONResponse(
        content=exc.response_msg,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
    )


@app.exception_handler(LogInitializationError)
def log_initialization_failed_handler(_, exc: LogInitializationError):
    """Return an error code and message if an error occurs in log initialization failure."""
    return JSONResponse(
        content=exc.response_msg,
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
    )


def _initialize_ope_id():
    """operationID initialization"""
    Task.__index_op_id__ = 0


@app.post(BASEURL + "migration-procedures", response_class=JSONResponse)
def create_migration_procedure(nodelayout: NodeLayout, background_tasks: BackgroundTasks):  # pylint: disable=C0103
    """Creating a migration procedure

    Args:
        nodelayout (NodeLayout):current layout and desired layout

    Returns:
        JSONResponse: migration procedure
    """
    logger = None
    logger = initialize_log()
    logger.info("Start running")
    logger.info(f"request param :{nodelayout}")
    bound_devices_map = nodelayout.desiredLayout.get("boundDevices", {})
    procedures = Plan.system_update_plan(
        prev=System.decode_json(nodelayout.currentLayout, bound_devices_map),
        new=System.decode_json(nodelayout.desiredLayout, bound_devices_map),
    )
    response = JSONResponse(status_code=HTTPStatus.OK.value, content=procedures.encode_json())
    background_tasks.add_task(_initialize_ope_id)
    logger.info("Completed successfully")
    return response


def main():
    """entry point"""
    try:
        server_config = MigrationConfigReader().migration_procedures_config
        uvicorn.run(app, **server_config)
    except CustomBaseException as err:
        err.output_stderr()
    except KeyboardInterrupt:
        pass
