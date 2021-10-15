# -*- coding: utf-8 -*-
# -*- Python Version: 3.9 -*-

"""Setup the loggers, set configuration and formatting."""

import pathlib
import logging
import os

LOG_DIR = pathlib.Path(".", "logs")
LOG_FILE_HBJSON = LOG_DIR / "log_HBJSON_to_PHX.log"


def get_log_file_path() -> pathlib.Path:
    """Set up the Log folder and file, if they don't exist

    Returns:
    --------
        * (pathlib.Path) The path to the log file
    """

    # -- Folder
    if not os.path.exists(LOG_FILE_HBJSON.parent):
        os.makedirs(LOG_FILE_HBJSON.parent)

    # -- File
    if not os.path.exists(LOG_FILE_HBJSON):
        with open(LOG_FILE_HBJSON, mode="w"):
            pass

    return LOG_FILE_HBJSON


def config_loggers(level="debug") -> None:
    """Create the Loggers, configure settings and formatting"""

    log_file_path = get_log_file_path()
    logger = logging.getLogger("HBJSON")

    # -- Clear out the exiting log-file contents
    with open(log_file_path, "r+") as f:
        f.truncate(0)

    # -- Set the FileHandler, Formatting
    file_handler = logging.FileHandler(log_file_path, mode="a", encoding="utf-8", delay=True)
    logger.addHandler(file_handler)
    file_handler.flush()

    # -- Set the log level
    if level.upper() == "INFO":
        logger.setLevel(logging.INFO)
    elif level.upper() == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif level.upper() == "WARNING":
        logger.setLevel(logging.WARNING)
    elif level.upper() == "CRITICAL":
        logger.setLevel(logging.CRITICAL)
