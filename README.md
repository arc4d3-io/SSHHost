# SSHHost Class

This is an SSHHost class written in Python, designed to manage remote SSH connections to hosts. It uses the Paramiko library to handle SSH connections, allowing users to load SSH keys, execute commands, and update user passwords on remote hosts.

## Features

- Connect to remote hosts using SSH
- Generate a random password for users
- Execute commands on remote hosts
- Load SSH keys for authentication
- Update user passwords

## Usage

1. Import the `SSHHost` class in your script
2. Create an instance of the `SSHHost` class with the target host's IP, username, and password
3. Use the provided methods to interact with the remote host

```python
from ssh_host import SSHHost

ip = "192.168.1.1"
username = "user"
password = "pass"

ssh_host = SSHHost(ip, username, password)
ssh_host.load_ssh_key()
ssh_host.update_user()
ssh_host.close()
```

## Methods

- `_generate_password`: Generate a random password with a given length
- `execute_command`: Execute a command on the remote host
- `close`: Close the SSH connection
- `load_ssh_key`: Load the public SSH key and save it to the remote host's `authorized_keys` file
- `update_user`: Update the user's password on the remote host

## Dependencies

- Python 3
- `paramiko`
- `os`
- `socket`
- `secrets`
- `string`
- `models.logger` (a custom logger module)