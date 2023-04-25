import paramiko
import os
import socket
import secrets
import string
from logger import Logger

class SSHHost:

    def __init__(self, ip, username, password):
        self.ssh_public_key_path = os.path.expanduser("~/.ssh/id_rsa.pub")
        self.known_host_path = os.path.expanduser('~/.ssh/known_hosts')
        self.ip = ip
        self.username = username
        self.password = password
        self.logger = Logger()        
        self.new_password = self._generate_password()
        try:
            self.client = paramiko.SSHClient()
            self.client.load_host_keys(self.known_host_path)
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.ip, username=self.username, password=self.password)

        except paramiko.AuthenticationException:
            self.logger.log(f"FAIL - [{self.ip}] falha na autenticação - abortando")                  
            exit(1)
        except socket.gaierror:
            pass

    def _generate_password(self,length=24):
        characters = string.ascii_letters + string.digits + string.punctuation
        password = ''.join(secrets.choice(characters) for _ in range(length))
        return password

    def execute_command(self, command):
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.channel.recv_exit_status()

    def close(self):
        self.client.close()

    def load_ssh_key(self):
        with open(self.ssh_public_key_path, 'r') as file:
            public_key = file.read().strip()

        self.client.exec_command("mkdir -p ~/.ssh")
        self.client.exec_command(f"echo '{public_key}' >> ~/.ssh/authorized_keys")
        self.client.exec_command("chmod 700 ~/.ssh")
        self.client.exec_command("chmod 600 ~/.ssh/authorized_keys")

        self.logger.log(f"OK - [{self.ip}] SSH_KEY salva") 

    def update_user(self):
        comando = f"(echo '{self.new_password}'; echo '{self.new_password}')  |sudo  passwd {self.username}"
        if self.execute_command(comando) > 0:
        # Verificar se a senha foi alterada com sucesso
          self.logger.log(f"FAIL - [{self.ip}] falha ao executar comando {comando}")                 
          return False
        else:
            self.logger.log(f"OK - [{self.ip}] usuário: [{self.username}] senha: [{self.new_password}]")                                          
            return True     