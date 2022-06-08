import pexpect


def show_version(device,ip, user, password):
    child = pexpect.spawn('telnet ' + ip)
    child.expect('Username:')
    child.sendline(user)
    child.expect('Password:')
    child.sendline(password)
    child.expect(device+'#')
    child.sendline('show version | i V')
    child.expect(device+'#')
    result = child.before
    child.sendline('exit')
    return device, result

if __name__ == '__main__':
    user = 'cisco'
    password = 'cisco'
    print(show_version('R1', '192.168.1.6',user, password))
    print(show_version('R2', '192.168.1.10', user, password))
    print(show_version('R3', '192.168.1.14', user, password))
    print(show_version('R5-tor', '192.168.1.1', user, password))
    print(show_version('R6-edge', '192.168.1.18', user, password))

