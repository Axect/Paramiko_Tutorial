import paramiko

common_key_path = '$HOME/.ssh/id_rsa'

# SSH server configuration
servers = [
    {
        'host': '<IP address for the first server>',
        'port': 22,
        'user': 'axect',
        'key_path': common_key_path,
    },
    {
        'host': '<IP address for the second server>',
        'port': 22,
        'user': 'axect',
        'key_path': common_key_path,
    },
    {
        'host': '<IP address for the third server>',
        'port': 22,
        'user': 'axect',
        'key_path': common_key_path,
    }
]

# Initialize the SSH client for the first server
client1 = paramiko.SSHClient()
client1.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the first server
client1.connect(servers[0]['host'], port=servers[0]['port'], username=servers[0]['user'], key_filename=servers[0]['key_path'])

# Initialize the SSH client for the second server
client2 = paramiko.SSHClient()
client2.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the second server via the first server
sock1 = client1.get_transport().open_channel("direct-tcpip", (servers[1]['host'], servers[1]['port']), (servers[0]['host'], servers[0]['port']))
client2.connect(servers[1]['host'], port=servers[1]['port'], username=servers[1]['user'], key_filename=servers[1]['key_path'], sock=sock1)

# Initialize the SSH client for the third server
client3 = paramiko.SSHClient()
client3.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Connect to the third server via the second server
sock2 = client2.get_transport().open_channel("direct-tcpip", (servers[2]['host'], servers[2]['port']), (servers[1]['host'], servers[1]['port']))
client3.connect(servers[2]['host'], port=servers[2]['port'], username=servers[2]['user'], key_filename=servers[2]['key_path'], sock=sock2)

# Execute a command on the third server (ls -l)
stdin, stdout, stderr = client3.exec_command('ls -l')
print(stdout.read().decode('utf-8'))

# Close the SSH connections
client3.close()
client2.close()
client1.close()
