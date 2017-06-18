#!/usr/bin/env python

import subprocess
import json


# Open new terminal and connect to host
def connect(hostname, port, username, password):
    # bash command to connect to host
    return subprocess.Popen("gnome-terminal --window-with-profile=TERMINAL-SCRIPT --geometry 118x30 -x sh -c \"sshpass -p {0} ssh -o StrictHostKeyChecking=no -p {1} -l {2} {3}\"".format(password, port, username, hostname), shell=True)


# Get ssh host information from the specific host file
def get_hosts(json_file):
    with open (json_file) as host_file:
        host_dict = json.load(host_file)
    return host_dict


def main():
    while True:
        key_list = get_hosts('example_hosts.json')
        for idx, key in enumerate(key_list):
            print "{0}: {1}".format(idx, key.upper())
        else:
            quit_idx = idx + 1
            print "{0}: QUIT".format(quit_idx)
        # Get user input to connect to device
        option = raw_input("ENTER OPTION (0-{0}) ==> ".format(quit_idx))
        # Provides a number of ways to break from for loop
        if option.lower() == "quit" or option.isdigit() and int(option) == quit_idx:
            break
        elif option.isdigit() and int(option) < quit_idx:
            while True:
                for idx, key in enumerate(key_list.items()[int(option)][1]):
                    print "{0}: {1}".format(idx, key.upper())
                else:
                    quit_idx = idx + 1
                    print "{0}: QUIT".format(quit_idx)
                get_device = raw_input("ENTER OPTION (0-{0}) ==> ".format(quit_idx))
                if get_device.lower() == "quit" or get_device.isdigit() and int(get_device) == quit_idx:
                    break
                elif get_device.isdigit() and int(get_device) < quit_idx:
                    top_level_menu = key_list.items()[int(option)][1]
                    device = top_level_menu.items()[int(get_device)]
                    print("\n\n ===> CONNECTING TO {0}...\n\n".format(device[0].upper()))
                    #connect to user defined host
                    connect(device[1]['ipAddress'], device[1]['port'], device[1]['username'], device[1]['password'])
                else:
                    True
        else:
            True

if __name__ == "__main__":
    main()

