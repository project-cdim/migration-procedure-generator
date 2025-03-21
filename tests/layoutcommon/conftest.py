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
import os

import pytest

# NOTICE: Add the dummy server's IP/HOST to the NO_PROXY environment variable.
TEST_HOST = "localhost"
os.environ["NO_PROXY"] = TEST_HOST


@pytest.fixture(scope="session")
def httpserver_listen_address():
    """Change the IP and port of the dummy server created with pytest-httpserver.
    By default, the IP is localhost and the port is a randomly available port above 1024.
    If there is a need to fix the port, for example,
    because the target of the test loads port settings from a configuration file, define it in conftest.py.
    Ref: https://pytest-httpserver.readthedocs.io/en/latest/howto.html#customizing-host-and-port

    Returns:
        tuple : (IP, Port)
    """
    return (TEST_HOST, 8888)
