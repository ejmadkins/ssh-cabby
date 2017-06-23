# SSH Manager

A CLI based terminal manager for SSH clients that groups devices based on the structure defined in the specified host file.  The tool works in both Linux (tested on Ubuntu) and OSX environments.

1. Add host devices organised into groups to a specified host file:

```
{
   "Group-1":{
      "example-device-1":{
         "ipAddress":"10.0.0.1",
         "port":"22",
         "username":"username",
         "password":"password"
      },
      "example-device-2":{
         "ipAddress":"10.0.0.2",
         "port":"22",
         "username":"username",
         "password":"password"
      }
   },
   "Group-2":{
      "example-device-3":{
         "ipAddress":"10.0.0.3",
         "port":"22",
         "username":"username",
         "password":"password"
      },
      "example-device-4":{
         "ipAddress":"10.0.0.4",
         "port":"22",
         "username":"username",
         "password":"password"
      }
   }
}
```

2. Execute the ssh_manager.py script:

`python ssh_manager.py`

3. Select a group based on the group ID:

```
0: GROUP-1
1: GROUP-2
2: QUIT
ENTER group (0-2) ==> 0
```

4. Select a device based on the device ID:

```
0: EXAMPLE-DEVICE-2
1: EXAMPLE-DEVICE-3
2: EXAMPLE-DEVICE-1
3: QUIT
ENTER group (0-3) ==> 1


 ===> CONNECTING TO EXAMPLE-DEVICE-3...
```

5. To quit gracefully, either type the corresponding value listed next to quit or type "quit":

```
0: GROUP-1
1: GROUP-2
2: QUIT
ENTER group (0-2) ==> 2
```
