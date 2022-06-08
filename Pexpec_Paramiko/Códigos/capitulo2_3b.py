import paramiko
llave = paramiko.RSAKey.from_private_key_file('/home/echou/.ssh/id_rsa')
cliente = paramiko.SSHClient()
cliente.set_missing_host_key_policy(paramiko.AutoAddPolicy())
cliente.connect('192.168.199.182', username='cisco', pkey=llave)
stdin, stdout, stderr = cliente.exec_comando('ls -l')
stdout.read()
stdin, stdout, stderr = cliente.exec_command('pwd')
stdout.read()
cliente.close()

