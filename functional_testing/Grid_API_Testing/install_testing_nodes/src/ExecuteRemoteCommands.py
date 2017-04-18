import paramiko, time
from install_testing_nodes.src.RequestEnvAPI import RequestEnvAPI
from termcolor import colored


class ExecuteRemoteCommands(RequestEnvAPI):
    def __init__(self):
        super(ExecuteRemoteCommands, self).__init__()
        self.username = 'cloudscalers'
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def execute_command(self, command, skip_error=False):
        try:
            stdin, stdout, stderr = self.ssh.exec_command(command)
            tracback = stdout.readlines()
            if len(tracback) != 0:
                self.logging.info(' [+] Done!\n')
                print(colored(' [+] Done!\n', 'green'))
            elif not skip_error:
                self.logging.info(' [-] Failed!' % tracback)
                print(colored(' [-] Failed!' % tracback, 'red'))
            return tracback
        except:
            self.logging.error(" [-] ERROR : Can't execute %s command\n" % command)
            print(colored(" [-] ERROR : Can't execute %s command\n" % command, 'red'))

    def trasport_file(self, filepath):
        self.sftp = self.ssh.open_sftp()
        file_name = filepath.split('/')[-1]
        self.sftp.put(filepath, file_name)

    def connect_to_virtual_machine(self, port):
        self.logging.info(' [*] Connecting to the virtual machine .. ')
        print(colored(' [*] Connecting to the virtual machine .. ', 'white'))
        for _ in range(100):
            try:
                self.ssh.connect(self.cloudspace['ip'], port=port, username=self.username,
                                 password=self.virtualmachine['password'])
                self.logging.info(' [+] Connected!\n')
                print(colored(' [+] Connected!\n', 'green'))
                break
            except:
                time.sleep(2)
                self.logging.info(' [*] Trying to connect to the virtual machine .. ')
        else:
            self.ssh.connect(self.cloudspace['ip'], port=port, username=self.username,
                             password=self.virtualmachine['password'])

    def update_machine(self):
        self.logging.info(' [*] Updating virtual machine OS ... ')
        print(colored(' [*] Updating virtual machine OS ... ', 'white'))
        command = 'echo %s | sudo -S apt-get -y update' % self.virtualmachine['password']
        self.execute_command(command=command)

    def install_docker(self):
        self.logging.info(' [*] Installing docker  ... ')
        print(colored(' [*] Installing docker  ... ', 'white'))
        command = 'echo %s | sudo -S apt-get -y install docker docker.io' % self.virtualmachine['password']
        self.execute_command(command=command)

    def install_g8os(self):
        self.logging.info(' [*] Installing g8os .... ')
        print(colored(' [*] Installing g8os .... ', 'white'))
        command = 'echo %s | sudo -S docker run --privileged -d --name core -p 6379:6379 g8os/g8os-dev:1.0' % \
                  self.virtualmachine['password']
        self.execute_command(command=command)

    def install_jumpscale(self, branch):
        self.logging.info(' [*] Installing jumpscale .... ')
        print(colored(' [*] Installing jumpscale .... ', 'white'))
        command = """echo 'cd /tmp && export JSBRANCH="%s" && curl -k https://raw.githubusercontent.com/Jumpscale/jumpscale_core8/$JSBRANCH/install/install.sh?$RANDOM > install.sh && bash install.sh' > jsInstaller.sh""" % branch
        self.execute_command(command=command, skip_error=True)
        # command = 'echo %s | sudo -S bash jsInstaller.sh' % self.virtualmachine['password']
        command = """ echo %s | sudo -S bash -c "tmux new-session -d -s installJS 'bash jsInstaller.sh; bash -i'" """ % \
                  self.virtualmachine['password']
        self.execute_command(command=command, skip_error=True)

        for _ in range(15):
            command = 'which js'
            tracback = self.execute_command(command=command, skip_error=True)
            if not tracback:
                time.sleep(60)
            else:
                break
        else:
            self.logging.info(' [-] Failed!')
            print(colored(' [-] Failed!', 'red'))

    def install_g8core_python_client(self):
        self.logging.info(' [*] Installing g8core python client .... ')
        print(colored(' [*] Installing g8core python client .... ', 'white'))
        # command = """echo echo 'cd $TMPDIR;\ngit clone https://github.com/g8os/core0/\ncd core0\ngit checkout %s\ncd pyclient\npip install .\n' > g8_python_client.sh""" % branch
        # self.execute_command(command=command, skip_error=True)

        # command = 'echo %s | sudo -S bash g8_python_client.sh' % self.virtualmachine['password']
        command = 'echo %s | sudo -S pip3 install g8core' % self.virtualmachine['password']
        self.execute_command(command=command)

    def start_AYS_server(self):
        self.logging.info(' [*] Starting AYS .... ')
        print(colored(' [*] Starting AYS .... ', 'white'))
        command = 'echo %s | sudo -S bash -c "ays start --bind 0.0.0.0 --debug" ' % self.virtualmachine['password']
        self.execute_command(command=command, skip_error=True)

        time.sleep(10)
        self.logging.info(' [*] Create grid repo .... ')
        print(colored(' [*] Create grid repo .... ', 'white'))
        command = 'echo %s | sudo -S bash -c "ays repo create --name grid --git http://github.com/user/repo" ' % \
                  self.virtualmachine['password']
        self.execute_command(command=command)

    def clone_ays_templates(self, branch):
        self.logging.info(' [*] Clone ays templates .... ')
        print(colored(' [*] Clone ays templates .... ', 'white'))
        command = """echo 'cd /opt/code && git clone https://github.com/g8os/grid/ && cd grid && git checkout %s && ays reload' > clone_ays_template.sh""" % branch
        self.execute_command(command=command, skip_error=True)

        command = 'echo %s | sudo -S bash clone_ays_template.sh' % self.virtualmachine['password']
        self.execute_command(command=command)

    def discover_g8os_nodes(self):
        self.logging.info(' [*] Discover g8os nodes .... ')
        print(colored(' [*] Discover g8os nodes .... ', 'white'))

        discovering_blueprint = self.get_discovering_blueprint()
        command = """echo 'cd /optvar/cockpit_repos/grid/ && printf "%s" > blueprints/discover_nodes && ays blueprint && ays run create --follow' > discover_g8os_nodes.sh""" % discovering_blueprint
        self.execute_command(command=command, skip_error=True)

        command = 'echo %s | sudo -S bash discover_g8os_nodes.sh' % self.virtualmachine['password']
        self.execute_command(command=command)

    def install_go(self):
        self.logging.info(' [*] Installing go 1.8 lang .... ')
        print(colored(' [*] Installing go 1.8 lang .... ', 'white'))
        command = """echo 'cd /tmp/ && curl -O https://storage.googleapis.com/golang/go1.8.linux-amd64.tar.gz && tar -xvf go1.8.linux-amd64.tar.gz && mv go /usr/local && echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.profile && chmod 774 ~/.profile &&  ~/.profile && ln -fs /usr/local/go/bin/go /usr/bin/go' > Install_Go_1_8.sh """
        self.execute_command(command=command, skip_error=True)
        command = 'echo %s | sudo -S bash Install_Go_1_8.sh' % self.virtualmachine['password']
        self.execute_command(command=command)

    def start_API_server(self, API_branch, ays_server_ip):
        self.logging.info(' [*] Starting %s G8OS Grid API ..... ' % API_branch)
        print(colored(' [*] Starting %s G8OS Grid API ..... ' % API_branch, 'white'))
        command = """ echo 'mkdir -p /opt/code/ && cd /opt/code/ && export GOPATH='/opt/code/' && go get github.com/g8os/grid; cd src/github.com/g8os/grid/ && git checkout %s && git pull && cd api && export GOPATH=/opt/code/ && go get && go install && /opt/code/bin/api --bind :8080 --ays-url http://%s:5000 --ays-repo grid&' > start_api_server.sh """ % (
            API_branch, ays_server_ip)
        self.execute_command(command, skip_error=True)
        command = 'echo %s | sudo -S bash start_api_server.sh' % self.virtualmachine['password']
        self.execute_command(command=command)
