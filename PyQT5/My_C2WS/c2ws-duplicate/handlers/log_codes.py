#################################################################################
# Copyright: EC Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: log_codes.py
# Code Management Tool File Version: 03.05.00.00
# Date: 21/12/2022 
# SDD component: C2WS
# Purpose: Logging class to syslog
# Implemented Requirements: Python3
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 01.00.00.00   | 23/08/2022    | GMV - GCS Cybersecurity team  | First creation
# 03.05.00.00   | 21/12/2022    | GMV - GCS Cybersecurity team  | Added new error code
#################################################################################

import logging

LOG_CODES = {
    "GAL.GCS.GCSS.C2WS.SSH_AGENT_DETECTED" : {
        "msg" : "Agent SOCK: {} PID: {}",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.NOT_A_VALID_SSH_SESSION" : {
        "msg" : "Not a valid SSH Agent session",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.ERROR_CONFIG_FILE" : {
        "msg" : "Missing key {} in section {}. Include it in the format key:value.",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.VALID_SSH_SESSION" : {
        "msg" : "Valid SSH Agent session",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.SSH_AGENT_FILE_FOUND" : {
        "msg" : "SSH Agent file found, checking if it's a valid session",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.LOGIN_PROCESS_START" : {
        "msg" : "Started login process",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.INCORRECT_CREDENTIALS" : {
        "msg" : "Incorrect credentials for user : {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.LOADING_KEYS" : {
        "msg" : "Loading keys for user : {}",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.COULD_NOT_GET_KEYS" : {
        "msg" : "Couldn't get keys",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.SSH_AGENT_CONNECTED" : {
        "msg" : "Connected to the SSH Agent",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.SSH_KEY_ADDED" : {
        "msg" : "SSH Key added",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.C2WSD_UNEXPECTED_ERROR" : {
        "msg" : "There was an unexpected error: {}",
        "level" : logging.CRITICAL
    },
    "GAL.GCS.GCSS.C2WS.USER_SESSIONS_CREATED" : {
        "msg" : "Created user sessions",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.CHECKING_SESSION_STATUS" : {
        "msg" : "Checking status for selected session",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.SESSION_STATUS_CHECK_ERROR" : {
        "msg" : "Could not check session status: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.DISCONNECT_USER_ERROR" : {
        "msg" : "Could not disconnect user: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.USER_PRESS" : {
        "msg" : "User pressed: {}",
        "level" : logging.DEBUG
    },
    "GAL.GCS.GCSS.C2WS.USER_CONNECTION_CHECK" : {
        "msg" : "Checking if user can connect to nomachine...",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.STARTING_USER_CONNECTION" : {
        "msg" : "Connecting user",
        "level" : logging.DEBUG
    },
    "GAL.GCS.GCSS.C2WS.ERROR_CHECKING_USER_CONNECTION" : {
        "msg" : "Could not check whether the user can connnect to nomachine: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.SCREENSAVER_CHANGED" : {
        "msg" : "User changed screensaver time",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.ERROR_CONNECTING" : {
        "msg" : "Could not connect to NX session: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.NON_DEFAULT_WKS_SELECTED" : {
        "msg" : "User selected non default workstation",
        "level" : logging.WARNING
    },
    "GAL.GCS.GCSS.C2WS.OPENING_NX_SESSION" : {
        "msg" : "Tryng to open nomachine session",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.PROTOCOL_DETECTED" : {
        "msg" : "Protocol {} detected",
        "level" : logging.DEBUG
    },
    "GAL.GCS.GCSS.C2WS.CHECKING_CURRENT_NX_SESSIONS" : {
        "msg" : "Checking current sessions",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.ERROR_CHECKING_CURRENT_NX_SESSIONS" : {
        "msg" : "Could not check current sessions: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.ERROR_CONNECTING_VIA_RDP" : {
        "msg" : "Could not connect via RDP: {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.NO_PROTOCOL_DETECTED" : {
        "msg" : "No protocol detected for connection",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.NO_AVAILABLE_SESSIONS" : {
        "msg" : "There are no available sessions in this workstation",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.USER_CAN_KILL_SESSIONS" : {
        "msg" : "User has permissions to kill sessions",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.USER_CAN_NOT_KILL_SESSIONS" : {
        "msg" : "User does not have permissions to kill sessions",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.GENERATING_AVAILABLE_SESSIONS" : {
        "msg" : "Generating available sessions for user",
        "level" : logging.INFO
    },
    "GAL.GCS.GCSS.C2WS.ERROR_READING_SESSIONS" : {
        "msg" : "Error reading some sessions",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.USER_SESSION_ERROR" : {
        "msg" : "Error with sessions of user {}",
        "level" : logging.ERROR
    },
    "GAL.GCS.GCSS.C2WS.USER_SESSION_SET" : {
        "msg" : "Setting user sessions",
        "level" : logging.DEBUG
    },
    "GAL.GCS.GCSS.C2WS.USER_SESSION_LOAD" : {
        "msg" : "Loading user sessions",
        "level" : logging.DEBUG
    },
    "GAL.GCS.GCSS.C2WS.FIRST_SESSION_FOR_USER" : {
        "msg" : "First session for current user",
        "level" : logging.DEBUG
    }
}