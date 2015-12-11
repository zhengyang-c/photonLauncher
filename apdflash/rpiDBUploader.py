import os, json, sys
import paramiko
import shutil

"""
project strings to pass to rpiDBUploader:
- apdflash
- ghosts
- FeelsBadMan (no I'm joking)

"""

class rpiDBUploader():
    def __init__(self, filepath, project):

        self.ssh = paramiko.SSHClient()
        self.filepath = filepath
        self.project = project

        robinIP = "192.168.2.188"
        username = "robin"
        password = "freeasinfreedom"

        self.projects = {
        "apdflash": "Hsin Yee [SRP]",
        "ghosts": "GhostImaging"
        }

        self.ssh.connect(robinIP, username = username, password = password)
    def upload(self):
        # hard coded lmao
        shutil.copy(self.filepath, os.path.join("/mnt/photonics", self.filepath))
        c = 0
        while 1:
            ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("ls /mnt/photonics | grep {}".format(self.filepath))
            if ssh_stdout == self.filepath:
                ssh_stdin, ssh_stdout, ssh_stderr = self.ssh.exec_command("cp /mnt/photonics/{0} /home/robin/Dropbox/hbar/{1}/{0}".format(self.filepath, self.projects[self.project]))
                print "Uploaded successfully. Quitting."
                break
            else:
                time.sleep(1)
                print "Waiting... "
                c += 1
                if c > 5:
                    print "Timeout after 5 seconds. Attempt to upload failed. Quitting"
