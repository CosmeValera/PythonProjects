#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: config_handler.py
# Code Management Tool File Version: 03.05.00.00
# Date: 21/12/2022
# SDD component: C2WS
# Purpose: C2WS config handler
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
# 03.02.00.01   | 01/07/2022    | GMV - GCS Cybersecurity team  | Adapt to work with new c2ws-openldap-integration & read screen config
# 03.05.00.00   | 21/12/2022    | GMV - GCS Cybersecurity team  | Remove domain field
# 03.06.00.01   | 30/05/2023    | GMV - GCS Cybersecurity team  | Changed message and dialog management
#################################################################################

import configparser
import json

class ConfigHandler():

    MESSAGES_JSON = "/usr/share/c2ws/messages.json"
    CONFIG_INI = "/etc/c2ws/config.ini"

    def __init__(self):
        self.enabled_elements = {}
        self.work_stations = {}
        self.thinclient_info = {}

        self.separator_config = ","

        self.messages = {}


    def _split_elements(self, element):
        return list(map(str.strip, element[1].split(self.separator_config))) if self.separator_config in element[1] else [element[1]]


    def read_minipc_config(self, path=CONFIG_INI):
        config = configparser.ConfigParser()
        config.read(path)
        
        if config.has_section('EnabledElements'):
            for element in config.items('EnabledElements'):
                self.enabled_elements[element[0]] = self._split_elements(element) 

        if config.has_section('WorkStations'):
            for element in config.items('WorkStations'):
                self.work_stations[element[0]] = self._split_elements(element) 
        
        if config.has_section('Thinclient'):
            for element in config.items('Thinclient'):
                self.thinclient_info[element[0]] = element[1]


    def load_messages(self, path=MESSAGES_JSON):
        with open(path, 'r') as f:
            self.messages = json.load(f)


def main():
    ConfigHandler()

if __name__ == "__main__":
    main()
