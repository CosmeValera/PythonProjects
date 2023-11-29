#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: nomachine_handler.py
# Code Management Tool File Version: 03.05.00.00
# Date: 21/12/2022
# SDD component: C2WS
# Purpose: C2WS nomachine handler
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
# 03.02.00.00   | 22/04/2022    | GMV - GCS Cybersecurity team  | Add last connection
# 03.02.00.01   | 01/07/2022    | GMV - GCS Cybersecurity team  | Adapt to work with new c2ws-openldap-integration & read screen config
# 03.05.00.00   | 21/12/2022    | GMV - GCS Cybersecurity team  | Added screen config management & fix RDP command
#################################################################################

from handlers import SSHHandler
import subprocess
import config as CONFIG
from os.path import exists
import getpass
from pathlib import Path
import re
import datetime
import os

class NoMachineHandler():

    def __init__(self, ws, user, screens):
        self.ws = ws
        self.user = user
        self.minipc_user = getpass.getuser()
        self.screens = int(screens)

    def open_nomachine(self):
        user_home = os.path.expanduser('~')
        new_session_path = os.path.join(user_home, CONFIG.NEW_SESSION)
        Path(new_session_path).mkdir(exist_ok=True)
        new_session_file = new_session_path + self.ws + "_" + self.user + ".nxs"  
    
        if not exists(new_session_file):
            with open(CONFIG.TEMPLATE_NOMACHINE, "r") as file_template:
                lines = file_template.read()

            lines = self.search_and_change("Server host", self.ws, lines)
            lines = self.search_and_change("User", self.user, lines)
            lines = self.search_and_change("Private key for NX authentication", os.path.join(user_home, "/.ssh/id_rsa"), lines)

            if self.screens > 1:
                lines = self.search_and_change("Session window state", "multiscreen", lines)
                lines = self.search_and_change("Use custom resolution", "true", lines)
                lines = self.search_and_change("Resolution width",  str(self.screens * 1920), lines)

            with open(new_session_file, "w+") as new_session:
                new_session.write(lines)    
            
        elif exists(new_session_file):
            self.change_template(new_session_file)

        out = subprocess.Popen(["/usr/NX/bin/nxplayer", "--exit", "--hide", "--session", new_session_file])


    
    def change_template(self, created_session_file):
        with open(created_session_file,"r") as f:
            lines = f.read()

        lines = self.search_and_change("Session window state", "multiscreen", lines)

        with open(created_session_file,"w") as f:
            f.write(lines)


    def search_and_change(self, key, value, lines):

        lines = lines.strip()
        regex = '\"' + key + '\" value\=\"\w*\"'
        replace = '"' + key + '" value="' + value + '"'
        lines = re.sub(regex, replace, lines)

        return lines


    def open_console(self):
        subprocess.Popen(["xterm", "-e", "ssh", "-A", self.user + "@" + self.ws])


    def send_message_to_user(self, user_id, message):
        # Send message to that session
        if (user_id != ""):
            return SSHHandler.run_remote_command(self.user, self.ws, 'sudo /etc/NX/nxserver --message ' + user_id + ' ' + message) 


    def terminate_user(self, user_id):
        if (user_id != ""):
            return SSHHandler.run_remote_command(self.user, self.ws, 'sudo /etc/NX/nxserver --terminate ' + user_id)


    def disconnect_user(self, user_id):
        if (user_id != ""):
            return SSHHandler.run_remote_command(self.user, self.ws, 'sudo /etc/NX/nxserver --disconnect ' + user_id)


    def connected_sessions(self):
        sessions = []
        messages, err = SSHHandler.run_remote_command(self.user, self.ws, 'sudo /etc/NX/nxserver --history')
        ls = messages.split('\n')

        disconnected = list(filter(lambda element: 'Disconnected' in element, ls))
        connected = list(filter(lambda element: 'Connected' in element, ls))

        if ".Xauthority" in err:
            err = ""

        if "Could not chdir to home directory" in err:
            err = "Could not connect to " + self.ws +" with user " + self.user + ", not properly configured (missing home directory).\nTalk to an administrator to finish required configurations."

        for disc in disconnected:
            lc = "-"
            disc_s = disc.split() 
            if len(connected) == 0:
                sessions.append([disc_s[1], disc_s[3], disc_s[6], disc_s[2], lc])
            for conn in connected:
                conn_s = conn.split() 
                today = False
                # If the user is the same, the session is connected
                if conn_s[1] == disc_s[1]:
                    if conn_s[4] == datetime.datetime.now().strftime("%Y-%m-%d"):
                        today = True
                    lc = "From " + (conn_s[5] if today else conn_s[4] + " " + conn_s[5])
                    sessions.append([conn_s[1], conn_s[3], conn_s[6], conn_s[2], lc])
                    break
                elif conn == connected[-1]:
                    sessions.append([disc_s[1], disc_s[3], disc_s[6], disc_s[2], lc])

        return sessions, err
        

    def get_session_info(self):
        session_total, err = self.connected_sessions()
        session = ""
        for i in session_total:
            if self.user in i:
                session = i
        if session == "":
            return "Closed", err
        else:
            return session[2], err


    def open_rdp(self):
        return SSHHandler.run_command(["xfreerdp", "/v:" + self.ws + ":3389", "/sec:tls", "/cert-tofu"])