#!/usr/bin/python3

import getpass
from pexpect import pxssh

devices = {'iosv-1': {'prompt': 'iosv-1#', 'ip': '192.168.0.1'}, 
           'iosv-2': {'prompt': 'iosv-2#', 'ip': '172.16.1.21'}}
commands = ['term length 0', 'show version', 'show run']

username = input('Usuario: ')
password = getpass.getpass('Password: ')

# Iniciamos el ciclo para los dispositivos
for device in devices.keys(): 
    outputFileName = device + '_salida.txt'
    device_prompt = devices[device]['prompt']
    child = pxssh.pxssh()
    child.login(devices[device]['ip'], username.strip(), password.strip(), auto_prompt_reset=False)
    # Iniciamos el ciclo para el envio de comandos y el archivo de salida
    with open(outputFileName, 'wb') as f:
        for command in commands:
            child.sendline(command)
            child.expect(device_prompt)
            f.write(child.before)
    
    child.logout()


