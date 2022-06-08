#!/usr/bin/python3

import pexpect

devices = {'iosv-1': {'prompt': 'iosv-1#', 'ip': '172.16.1.20'}, 
           'iosv-2': {'prompt': 'iosv-2#', 'ip': '172.16.1.21'}}
username = 'cisco'
password = 'cisco'

for device in devices.keys(): 
    device_prompt = devices[device]['prompt']
    child = pexpect.spawn('telnet ' + devices[device]['ip'])
    child.expect('[Uu]sername:')
    child.sendline(username)
    child.expect(['Password:','password'])
    child.sendline(password)
    child.expect(device_prompt)
    child.sendline('show run | i hostname')
    child.expect(device_prompt)
    print(child.before)
#    print(str(child))
    print(child.before)
    child.sendline('exit')

    


    
    

