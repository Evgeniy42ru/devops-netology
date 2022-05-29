#!/usr/bin/env python3


import os
import sys


#Проверяем что указан путь к репозиторию
try:
    repoPath = sys.argv[1]
except IndexError:
    print("Необходимо указать путь к репозиторию.")
    exit(1)

#Проверяем что директория существует
if os.path.exists(repoPath) == False:
    print ("Директории не существует - " + repoPath)
    exit(1)

#Проверяем наличие гита 
bash_command = ["cd " + repoPath, "git status"]
result_os = os.popen(' && '.join(bash_command)).read()

if (result_os) == 'fatal: not a git repository (or any of the parent directories): .git':
    print(result_os)
    exit(1)

#Проверяем изменения
bash_command_pwd = ["cd " + repoPath, "pwd"]
general_path = os.popen(' && '.join(bash_command_pwd)).read().rstrip('\n')
is_change = False
for result in result_os.split('\n'):
    if result.find('modified') != -1:
        prepare_result = result.replace('\tmodified:   ', '')
        print(general_path + '/' + prepare_result)
        #break