#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: __init__.py
# Code Management Tool File Version: 03.01.00.00
# Date: 18/02/2022
# SDD component: C2WS
# Purpose: C2WS Handlers main imports
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
#################################################################################

import os
import sys

file_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, file_dir)

from config_handler import ConfigHandler
from ldap_handler import LDAPHandler
from logger import Logger

try: # Not needed for c2ws-server
    import ssh_handler as SSHHandler
    from nomachine_handler import NoMachineHandler
except:
    pass
