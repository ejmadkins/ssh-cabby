#!/usr/bin/env python

# Built-in modules
import json
import subprocess
import os
import argparse

__author__ = "Ed Adkins"
__copyright__ = "Copyright (C) 2017 Ed Adkins"
__license__ = "MIT"
__version__ = "1.0"


def get_host_file():
    """ Fetches host file based on user input

    Args:
        None

    Returns:
        A string of of the chosen host file:

        "host_file.json"
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="select the host file name", type=str, required=True)
    args = parser.parse_args()
    return(args.file)


def get_hosts(host_file):
    """ Fetches host data from a specified host_file

    Args:
        host_file: Device host file in JSON format

    Returns:
        A dict mapping keys to the corresponding host data, as follows:

        {u'Group-1':
            {u'example-device-2':
                {u'username': u'username',
                u'password': u'password',
                u'ipAddress': u'10.0.0.2',
                u'port': u'22'},
            u'example-device-3':
                {u'username': u'username',
                u'password': u'password',
                u'ipAddress': u'10.0.0.3',
                u'port': u'22'}
            }
        }
    """
    with open(os.path.join('./host_files', host_file), 'r') as host_file:
        return json.load(host_file)


def menu_level_selector(host_file, level, group):
    """ Selects corresponding menu level

    Args:
        host_file: Device host file in JSON format
        level: Specifies the current menu level
        group: Specifies the user selected group

    Returns:
        A list of strings representing either groups or devices:

        top-menu: [u'Group-1', u'Group-2']
        sub-menu: [u'example-device-2', u'example-device-3', u'example-device-1']
    """
    if level == 'top-menu':
        return [i for i in get_hosts(host_file)]
    return [i for i in get_hosts(host_file).values()[group]]


def print_menu(host_file, level='top-menu', group=1):
    """ Prints interactive menu to screen

    Args:
        host_file: Device host file in JSON format
        level: Optional variable that specifies the current menu level
        group: Another optional variable that specifies the user selected group

    Returns:
        A dict mapping keys to a user selected group and a value to exit

        {'user_input': '0', 'exit_value': 2}
    """
    for idx, key in enumerate(menu_level_selector(host_file, level, group)):
        print('{0}: {1}'.format(idx, key.upper()))
    else:
        quit_idx = idx + 1
        print('{0}: QUIT'.format(quit_idx))
    group = raw_input("ENTER group (0-{0}) ==> ".format(quit_idx))
    return {"user_input" : group, "exit_value" : quit_idx}


def connect_linux(hostname, port, username, password):
    """ Opens new terminal in a linux enviroment and connects to host

    Args:
        hostname: Device hostname
        port: TCP port number to be used for ssh connection
        username: Device username
        password: Device password

    Returns:
        A bash command to initiate a terminal session to the selected host
    """
    return subprocess.Popen('gnome-terminal --window-with-profile=TERMINAL-SCRIPT --geometry 118x30 -x sh -c \"sshpass -p {3} ssh -o StrictHostKeyChecking=no -p {1} -l {2} {0}\"'.format(hostname, port, username, password), shell=True)


def connect_osx(hostname, port, username):
    """ Opens new terminal in an OSX enviroment and connects to host

    Args:
        hostname: Device hostname
        port: TCP port number to be used for ssh connection
        username: Device username

    Returns:
        A bash command to initiate a terminal session to the selected host
    """
    return os.system('ssh -p {1} -l {2} {0}'.format(hostname, port, username))


def main(host_file):
    while True:
        menu = print_menu(host_file)
        if menu['user_input'].lower() == "quit" or menu['user_input'].isdigit() and int(menu['user_input']) == menu['exit_value']:
            break
        elif menu['user_input'].isdigit() and int(menu['user_input']) < menu['exit_value']:
            level = "sub-menu"
            sub_menu = print_menu(host_file, level, int(menu['user_input']))
            if sub_menu['user_input'].lower() == "quit" or sub_menu['user_input'].isdigit() and int(sub_menu['user_input']) == sub_menu['exit_value']:
                level = "top-menu"
            else:
                selected_group = get_hosts(host_file).values()[int(menu['user_input'])]
                selected_device = selected_group.items()[int(sub_menu['user_input'])]
                print('\n\n ===> CONNECTING TO {0}...\n\n'.format(selected_device[0].upper()))
                connect_osx(selected_device[1]['ipAddress'], selected_device[1]['port'], selected_device[1]['username'])


if __name__ == "__main__":
    # Verify that file exists, if so, call main()
    host_file = get_host_file()
    if os.path.isfile(os.path.join('./host_files', host_file)):
        main(host_file)
    else:
        print('> ERROR: \'{}\' does not exist'.format(host_file))
        print('> Files in the host_files directory:')
        for idx, file in enumerate(os.listdir('./host_files')):
            print('  {0}: {1}'.format(idx,file))
