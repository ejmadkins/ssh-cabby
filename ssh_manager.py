#!/usr/bin/env python

import json
import subprocess
import os


# open new terminal and connect to host
def connect_linux(hostname, port, username, password):
    # bash command to connect to host
    return subprocess.Popen("gnome-terminal --window-with-profile=TERMINAL-SCRIPT --geometry 118x30 -x sh -c \"sshpass -p {3} ssh -o StrictHostKeyChecking=no -p {1} -l {2} {0}\"".format(hostname, port, username, password), shell=True)


# open new terminal and connect to host
def connect_osx(hostname, port, username):
    return os.system('ssh -p {1} -l {2} {0}'.format(hostname, port, username))


# get host information from json file
def get_hosts(json_file):
    with open (os.path.join('./host_files', 'test_hosts.json'), 'r') as host_file:
        host_dict = json.load(host_file)
    return host_dict


# return host information for a given level of the menu
def menu_level_selector(key_list, level, option):
    if level == 'top-menu':
        return [i for i in get_hosts(key_list)]
    else:
        return [i for i in get_hosts(key_list).items()[option][1]]


# print menu level and return user input and the value to quit
def print_menu(key_list, level='top-menu', option=1):
    for idx, key in enumerate(menu_level_selector(key_list, level, option)):
        print("{0}: {1}".format(idx, key.upper()))
    else:
        quit_idx = idx + 1
        print("{0}: QUIT".format(quit_idx))
    option = raw_input("ENTER OPTION (0-{0}) ==> ".format(quit_idx))
    return {"user_input" : option, "exit_value" : quit_idx}


def main():
    key_list = 'example_hosts.json'
    while True:
        menu = print_menu(key_list)
        if menu['user_input'].lower() == "quit" or menu['user_input'].isdigit() and int(menu['user_input']) == menu['exit_value']:
            break
        elif menu['user_input'].isdigit() and int(menu['user_input']) < menu['exit_value']:
            level = 'sub-menu'
            sub_menu = print_menu(key_list, level, int(menu['user_input']))
            if sub_menu['user_input'].lower() == "quit" or sub_menu['user_input'].isdigit() and int(sub_menu['user_input']) == sub_menu['exit_value']:
                level = 'top-menu'
            else:
                selected_group = get_hosts(key_list).items()[int(menu['user_input'])][1]
                selected_device = selected_group.items()[int(sub_menu['user_input'])]
                print("\n\n ===> CONNECTING TO {0}...\n\n".format(selected_device[0].upper()))
                connect_osx(selected_device[1]['ipAddress'], selected_device[1]['port'], selected_device[1]['username'])


if __name__ == "__main__":
    main()