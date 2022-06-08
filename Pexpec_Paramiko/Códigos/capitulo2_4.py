#!/usr/bin/python3

import paramiko, getpass, time, json

with open('dispositivos.json', 'r') as f:
    hosts = json.load(f)

with open('comandos.txt', 'r') as f: 
    comandos = [line for line in f.readlines()]

usuario = input('Usuario: ')
password = getpass.getpass('Password: ')

max_buffer = 65535

def clear_buffer(conexion):
    if conexion.recv_ready():
        return conexion.recv(max_buffer)

# Iniciamos el ciclo para los dispositivos
for host in hosts.keys(): 
    nombreArchivo = host + '_salida.txt'
    conexion = paramiko.SSHClient()
    conexion.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    conexion.connect(hosts[host]['ip'], username=usuario, password=password, look_for_keys=False, allow_agent=False)
    nueva_conexion = conexion.invoke_shell()
    salida = clear_buffer(nueva_conexion)
    time.sleep(2)
    nueva_conexion.send("terminal length 0\n")
    salida = clear_buffer(nueva_conexion)
    with open(nombreArchivo, 'wb') as f:
        for comando in comandos:
            nueva_conexion.send(comando)
            time.sleep(2)
            salida = nueva_conexion.recv(max_buffer)
            print(salida)
            f.write(salida)
    
    nueva_conexion.close()
    
