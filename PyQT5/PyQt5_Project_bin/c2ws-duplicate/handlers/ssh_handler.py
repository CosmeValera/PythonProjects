#################################################################################
# Copyright: EU Proprietary Information. Unauthorized distribution, dissemination or disclosure not allowed.
# Project: GCS FOC2
# File: ssh_handler.py
# Code Management Tool File Version: 03.01.00.00
# Date: 15/12/2021
# SDD component: C2WS
# Purpose: C2WS ssh handler
# Implemented Requirements: Python3, NX, LDAP
# Language: Python
# Author: GMV - GCS Cybersecurity team
# History:
#
# Version       | Date          | Name                          | Change history 
# 03.01.00.00   | 18/02/2022    | GMV - GCS Cybersecurity team  | First version
#################################################################################

import subprocess
  
def run_command(cmd):
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.read().decode('utf-8'), proc.stderr.read().decode('utf-8')


def run_remote_command(user, host, cmd):
    out, err = run_command(["ssh","-q", "-o", "StrictHostKeyChecking=no", user+"@"+host, cmd])
    err = "\n".join([e for e in err.split("\n") if len(e) > 0 if e[0] != "#"])
    return out, err


def generate_new_keypair(userpasswd, keyfile):
    # ssh-keygen -b 4096 -N 'UserPasswd' -t rsa -f /my/file/name
    ssh_keygen_generate = ["ssh-keygen", "-b", "4096", "-N", userpasswd, "-t", "rsa", "-f", keyfile]
    out, err = run_command(ssh_keygen_generate)
    
    if err:
        raise Exception(err)
    else:
        return keyfile


def update_key_passphrase(newpasswd, oldpasswd, keyfile):
    # ssh-keygen -p -f /my/file/name -N 'NewPasswd' -P 'old passwd'
    ssh_keygen_update = ["ssh-keygen", "-p", "-f", keyfile, "-N", newpasswd, "-P", oldpasswd]

    out, err = run_command(ssh_keygen_update)

    if err:
        raise Exception(err)
    else:
            return keyfile