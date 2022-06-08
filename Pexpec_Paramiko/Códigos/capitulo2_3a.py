#!/usr/bin/python3

import paramiko, time

conexion = paramiko.SSHClient()
conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
conexion.connect('172.16.1.20', username='cisco', password='cisco', look_for_keys=False, allow_agent=False)
nueva_conexion = conexion.invoke_shell()
salida = nueva_conexion.recv(5000)
print(salida)
nueva_conexion.send("show version\n")
time.sleep(3)
salida = nueva_conexion.recv(5000)
print(salida)
nueva_conexion.close()
    

