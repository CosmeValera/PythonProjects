#################################################################################
# Copyright: EC Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: logger.py
# Code Management Tool File Version: 01.00.00.00
# Date: 23/08/2022 
# SDD component: C2WS
# Purpose: Logging class to syslog
# Implemented Requirements: Python3
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 01.00.00.00   | 23/08/2022    | GMV - GCS Cybersecurity team  | First creation
#################################################################################

import logging
import logging.handlers
import os

from log_codes import LOG_CODES

class Logger():

    DEFAULT_LOG_FORMAT = '%(name)s[%(process)d]: %(levelname)s - %(message)s'

    def __init__(self, name, level=logging.INFO, format=DEFAULT_LOG_FORMAT):
        self.name = name
        self.level = level
        self.format = format
        self.logger = self.generate_logger()
        

    def generate_logger(self):
        logger = logging.getLogger(self.name)
        logger.setLevel(self.level)

        if logger.handlers:
            return logger

        handler = logging.handlers.SysLogHandler(address="/dev/log")
        formatter = logging.Formatter(self.format)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        return logger


    def add_file_handler(self, path):
        handler = logging.handlers.WatchedFileHandler(path, mode="a", encoding="utf-8")
        formatter = logging.Formatter(self.format)
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

    
    def log(self, code, args=None):
        if type(args) == str:
            args = (args, )
            
        try:
            l = LOG_CODES[code]
            if args:
                message = l["msg"].format(*args)
            else:
                message = l["msg"]

            level = l["level"]
            message = "[{}] - {}".format(code, message)
        except TypeError as t:
            raise Exception("Logger.log args must be a iterable (touple or list)")
        except KeyError as k:
            raise Exception("Log code '{}' not found in the code dictionary or it's not correctly formatted".format(code))
        
        self.log_by_level(message, l["level"])


    def log_and_print(self, code, args=None):
        if type(args) == str:
            args = (args, )
            
        try:
            l = LOG_CODES[code]
            if args:
                message = l["msg"].format(*args)
            else:
                message = l["msg"]
                
            level = l["level"]
            message = "[{}] - {}".format(code, message)

            if level in [logging.ERROR, logging.CRITICAL]:
                print("[!]" + message)
            else:
                print(message)

        except TypeError as t:
            raise Exception("Logger.log args must be a iterable (touple or list)")
        except KeyError as k:
            raise Exception("Log code '{}' not found in the code dictionary or it's not correctly formatted".format(code))
        
        self.log_by_level(message, l["level"])
    

    def log_by_level(self, message, level):
        if level == logging.INFO:
            self.info(message)
        elif level == logging.WARNING:
            self.warning(message)
        elif level == logging.ERROR:
            self.error(message)
        elif level == logging.CRITICAL:
            self.critical(message)
        else:
            self.debug(message)
    

    def debug(self, message):
        self.logger.debug(message)
    

    def info(self, message):
        self.logger.info(message)


    def warning(self, message):
        self.logger.warning(message)


    def error(self, message):
        self.logger.error(message)
    

    def critical(self, message):
        self.logger.critical(message)