#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: ldap_handler.py
# Code Management Tool File Version: 03.02.00.00
# Date: 18/02/2022
# SDD component: C2WS
# Purpose: C2WS ldap handler
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
# 03.02.00.00   | 22/04/2022    | GMV - GCS Cybersecurity team  | Manage "self" in LDAP
# 03.02.00.01   | 01/07/2022    | GMV - GCS Cybersecurity team  | Adapt to work with new c2ws-openldap-integration
#################################################################################


import json
import hashlib
import base64
import re
import os
import collections
import subprocess

LDAP_QUERY_PATH = "/usr/bin/c2ws-ldap-query"
C2WS_PATH = os.path.join(os.path.expanduser("~"), ".c2ws")

CommandStruct = collections.namedtuple("CommandStruct", "stdout stderr returncode args")

class LDAPException(Exception):
    pass


class LDAPHandler():

    def __init__(self, user, password):
        self.user = user
        self.password = password
        self.user_passwd_file = os.path.join(C2WS_PATH.format(user), ".ldappwd")

        self.write_password()
    

    def __del__(self):
        self.delete_password()


    @staticmethod
    def run(cmd):
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        command = CommandStruct(args = cmd, 
                                returncode = proc.returncode,
                                stdout = proc.stdout.read().decode('utf-8'),
                                stderr = proc.stderr.read().decode('utf-8'))
        return command
    

    def write_password(self):
        c2ws_path = C2WS_PATH.format(self.user)
    
        if not os.path.isdir(c2ws_path):
            os.mkdir(c2ws_path)
            os.chmod(c2ws_path, 0o700)

        open(self.user_passwd_file, 'a').close()
        os.chmod(self.user_passwd_file, 0o600)
        with open(self.user_passwd_file, "w") as p:
            p.write(self.password)

    
    def delete_password(self):
        try:
            os.remove(self.user_passwd_file)
        except:
            pass


    def run_ldap_tool(self, args):
        cmd = [LDAP_QUERY_PATH, "--ldap-user", self.user, "--ldap-password-file", self.user_passwd_file]
        cmd += args

        cmd = self.run(cmd)

        return cmd


    def check_login(self):
        cmd = self.run_ldap_tool(["--check-login"])

        if "uid={}".format(self.user) in cmd.stdout:
            return True

        return False


    def get_user_keys(self):
        cmd = self.run_ldap_tool(["--user", "get", "--user-name", self.user])
        out = re.sub("\n ", "", cmd.stdout)
        priv_key = re.findall("sshPrivKey:: (\w+)", out)
        pub_key = re.findall("sshPublicKey:: (\w+)", out)
        
        if pub_key:
            pub_key = base64.b64decode(pub_key[0] + "==").decode('utf-8')
        else:
            pub_key = re.findall("sshPublicKey: (\w+)", out)

        if priv_key:
            priv_key = base64.b64decode(priv_key[0] + "==").decode('utf-8')
        else:
            priv_key = re.findall("sshPrivateKey: (\w+)", out)

        return priv_key, pub_key


    def get_user_sessions(self):
        user_sessions = []
        cmd = self.run_ldap_tool(["--group", "list"])
        all_groups = re.findall(f"cn=(\w+),ou=groups", cmd.stdout)

        for group in all_groups:
            cmd = self.run_ldap_tool(["--group", "get", "--group-name", group])
            if re.findall(f"memberUid: {self.user}", cmd.stdout):
                cmd = self.run_ldap_tool(["--fqdn", "list", "--group-name", group])
                fqdn_list = re.findall(f"fqdn=(.+?),cn=", cmd.stdout)

                for fqdn in fqdn_list:
                    cmd = self.run_ldap_tool(["--fqdn", "get", "--group-name", group, "--fqdn-name", fqdn])
                    auth_user_list = re.findall(f"sshAuthorizedUser: (.+)", cmd.stdout)

                    for ssh_user in auth_user_list:
                        if ssh_user == "self":
                            ssh_user = self.user

                        session = f"{ssh_user}@{fqdn}"
                        if session not in user_sessions:
                            user_sessions.append(session)

        return user_sessions
    

    def is_user_in_group(self, group):
        cmd = self.run_ldap_tool(["--group", "get", "--group-name", group])
        if re.findall(f"memberUid: {self.user}", cmd.stdout):
            return True