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

from migration_procedure_generator.setting import MigrationLogConfigReader, MigrationConfigReader, initialize_log
from migration_procedure_generator.common.logger import Logger
from migration_procedure_generator.custom_exception import SettingFileValidationError


class TestMigrationConfigReader:
    def test_success_read_configuration_file_and_interpret_settings(self):
        obj = MigrationConfigReader()
        log_obj = MigrationLogConfigReader()
        assert isinstance(log_obj.log_config, dict)
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

        base_config = {}
        config = {**base_config, **update_confg}
        mocker.patch("yaml.safe_load").return_value = config
        server = MigrationConfigReader().migration_procedures_config
        assert server == update_confg.get("migration_procedures")

    @pytest.mark.parametrize(
        "update_confg",
        [
            # Case where `logging_level` has an expected value
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "ERROR",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "ERROR",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "ERROR",
                    "handlers": ["file", "console"],

                }
            },
            {
                "log": {
                    "logging_level": "WARN",
                    "log_dir": "./",
                    "file": "app_layout_apply.log",
                    "rotation_size": 1000000,
                    "backup_files": 3,
                    "stdout": False,
                }
            },
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "CRITICAL",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "CRITICAL",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "CRITICAL",
                    "handlers": ["file", "console"],

                }
            },
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "DEBUG",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "DEBUG",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "DEBUG",
                    "handlers": ["file", "console"],

                }
            },
            # Case where `level` is missing
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        # "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            # Case where log directory specifies an existing path
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "./app_policy.log",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            # Case where `filename` has an expected value
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "./a",
                        "maxBytes": 100000000,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            # Case where `rotation_size` has a valid value
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 0,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            # Case where `backup_files` has a valid value
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 0,
                        "backupCount": 3,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file", "console"],

                }
            },
            # Case for `stdout` variations
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 0,
                        "backupCount": 72,
                        "encoding": "utf-8",
                    },
                    "console": {
                        "class": "logging.StreamHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "stream": "ext://sys.stdout",
                    },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file"],

                }
            },
            {
                "version": 1,
                "formatters": {
                    "standard": {
                        "format": "%(asctime)s %(levelname)s %(message)s",
                        "datefmt": "%Y/%m/%d %H:%M:%S.%f",
                    },
                },
                "handlers": {
                    "file": {
                        "class": "logging.handlers.RotatingFileHandler",
                        "level": "INFO",
                        "formatter": "standard",
                        "filename": "/var/log/cdim/app_policy.log",
                        "maxBytes": 0,
                        "backupCount": 72,
                        "encoding": "utf-8",
                        },
                },
                "root": {
                    "level": "INFO",
                    "handlers": ["file"],

                }
            },
        ],
    )
    def test_success_without_validation_error_from_logging_settings(self, mocker, update_confg):

        base_config = {
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
                    'filename': "/var/log/cdim/app_migration_procedures.log",
                    'maxBytes': 3000000,
                    'backupCount': 12,
                    'encoding': "utf-8"
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
        config = {**base_config, **update_confg}
        mocker.patch("yaml.safe_load").return_value = config
        MigrationLogConfigReader().log_config

    def test_log_config_failure_when_file_not_found_error(self, mocker):
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
                                'filename': '/lllllll/log/nec/gi/app_layout_apply.log',
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
        with pytest.raises(Exception):
            MigrationLogConfigReader().log_config

    def test_common_failure_when_migration_procedures_config_with_invalid_value(self, mocker):
        # Case where server configuration contains invalid values
        base_config = {
                "migration_procedures": {
                    "port": 8003,
                }
        }
        config = base_config
        mocker.patch("yaml.safe_load").return_value = config
        with pytest.raises(SettingFileValidationError) as e:
            MigrationConfigReader().migration_procedures_config


class TestLogger:
    @pytest.mark.parametrize(
        "log_level",
        [
            (
                {
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
                        'level': 'DEBUG',
                        'formatter': 'standard',
                        'filename': "/var/log/cdim/app_migration_procedures.log",
                        'maxBytes': 100000000,
                        'backupCount': 72,
                    },
                    'console': {
                        'class': 'logging.StreamHandler',
                        'level': 'DEBUG',
                        'formatter': 'standard',
                        'stream': 'ext://sys.stdout'
                    }
                },
                'root': {
                    'level': 'DEBUG',
                    'handlers': ['file']
                    }
            }
            ),  # log level:DEBUG
            (
                {
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
                        'level': 'WARN',
                        'formatter': 'standard',
                        'filename': "/var/log/cdim/app_migration_procedures.log",
                        'maxBytes': 100000000,
                        'backupCount': 72,
                    },
                },
                'root': {
                    'level': 'WARN',
                    'handlers': ['file']
                    }
            }
            ),  # log level:WARN
            (
                {
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
                        'level': 'ERROR',
                        'formatter': 'standard',
                        'filename': "/var/log/cdim/app_migration_procedures.log",
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
                    'level': 'ERROR',
                    'handlers': ['file']
                    }
            }
            ),  # log level:ERROR
            (
                {
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
                        'level': 'CRITICAL',
                        'formatter': 'standard',
                        'filename': "/var/log/cdim/app_migration_procedures.log",
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
                    'level': 'CRITICAL',
                    'handlers': ['file']
                    }
            }
            ),  # log level:CRITICAL
            (
                {
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
                        'filename': "/var/log/cdim/app_migration_procedures.log",
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
            ),  # log level:INFO
        ],
    )
    def test_logger_success_log_level_from_configuration_file(self, mocker, log_level):
        mocker.patch("yaml.safe_load").return_value = log_level
        glogger: Logger = initialize_log()
        log_level_str = logging.getLevelName(glogger._logger.getEffectiveLevel())
        log_level_str = "WARN" if log_level_str == "WARNING" else log_level_str
        assert log_level_str == log_level["handlers"]["file"]["level"]
