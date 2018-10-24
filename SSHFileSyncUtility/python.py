import paramiko
import json
from easygui import passwordbox
import os
from datetime import datetime
import time
import getpass
from os.path import splitext
import pathlib


def connect(server_address, port, user, password):
    print("User: {0}".format(user))
    print("Connecting with server: {0}".format(server_address))
    print("Port: {0}".format(port))

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.load_system_host_keys()
        ssh.connect(server_address, port, user, password)
        print("Connected with server ")
        return ssh
    except paramiko.ssh_exception.AuthenticationException:
        exit("Wrong user / password")
    except paramiko.ssh_exception.SSHException:
        exit("Cant connect with server")


def load_config():
    if os.path.isfile("config.json"):
        json_data = open("config.json")
        data = json.load(json_data)
        return data, passwordbox("Type password for the server: ")
    return None


def ignore_extension(filename):
    x = pathlib.Path(filename).suffix
    if x != "":
        x = x.split(".")
        for y in ignore:
            if x[1] == y:
                return False
    return True


def overwrite():
    for root, dirs, files in os.walk(local_folder):
        for filename in files:
            if ignore_extension(filename):
                try:
                    sftp.put(local_folder + filename, filename)
                    print("Overwrited file: " + filename)
                except IOError:
                    print("Error with " + filename)
        break


def update():
    for root, dirs, files in os.walk(local_folder):
        for filename in files:
            if ignore_extension(filename):
                try:
                    sftp.stat(filename) 
                    date1 = datetime.fromtimestamp(os.path.getmtime(local_folder + filename))
                    date2 = datetime.fromtimestamp(sftp.stat(filename).st_mtime)
                    date1 = time.mktime(date1.timetuple())
                    date2 = time.mktime(date2.timetuple())
                    if date1 > date2:
                        try:
                            sftp.put(local_folder + filename, filename)
                            print("Updated file: " + filename)
                        except IOError:
                            print("Error with " + filename)
                except IOError:
                    pass
        break


def add_non_existing():
    for root, dirs, files in os.walk(local_folder):
        for filename in files:
            if ignore_extension(filename):
                try:
                    sftp.stat(filename)
                except IOError:
                    try:
                        sftp.put(local_folder + filename, filename)
                        print("Added file: " + filename)
                    except IOError:
                        print("Error with " + filename)
        break


data, password = load_config()
if data is None:
    exit("Error with config file")

host = data["server_address"]
port = data["port"]
user = data["username"]
local_folder = data["local_folder"]
remote_folder = data["remote_folder"]
mode = data["mode"]
ignore = data["ignore"]

if not os.path.isdir(local_folder):
    exit("Local folder from config file does not exist")

ssh = connect(host, port, user, password)
sftp = ssh.open_sftp()

try:
    sftp.chdir(remote_folder)
except IOError:
    exit("Remote folder from config file does not exist!")


print("Mode: {0}".format(mode))
if mode == "overwrite":
    overwrite()
elif mode == "update":
    update()
elif mode == "add_non_existing":
    add_non_existing()
else:
    exit("Non existing mode in config file")

ssh.close()
