#!/usr/bin/env python3

import os

bash_command = ["cd ~/Projects/netology/devops-netology", "git status"]
bash_command_pwd = ["cd ~/Projects/netology/devops-netology", "pwd"]
result_os = os.popen(' && '.join(bash_command)).read()
general_path = os.popen(' && '.join(bash_command_pwd)).read().rstrip('\n')
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(general_path + '/' + prepare_result)
        #break