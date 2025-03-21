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
"""ExitCode constant"""

from enum import IntEnum, _simple_enum


@_simple_enum(IntEnum)
class ExitCode:
    """Defining constants for return values"""

    def __new__(cls, value):
        obj = int.__new__(cls, value)
        obj._value_ = value
        return obj

    # normal return value
    NORMAL = 0
    # validation error return value
    VALIDATION_ERROR = 1
    # config error return value
    CONFIG_ERROR = 2
    # internal error return value
    INTERNAL_ERR = 3
