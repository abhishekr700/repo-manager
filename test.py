# Modules needed
import json
import pathlib
from pathlib import Path
import urllib
import shutil
import os
import sys
from colorama import Fore, Back, Style, init
import subprocess
import argparse
import getpass

# My Imports
from commandLiveOutput import execCommandLive

# Colorama needs this to work on Windows
init()

################### 
# HELPER FUNCTIONS
###################

# Custom error handler for shutil.rmtree
def onerror(func, path, exc_info):
    """
    Error handler for ``shutil.rmtree``.

    If the error is due to an access error (read only file)
    it attempts to add write permission and then retries.

    If the error is for another reason it re-raises the error.
    
    Usage : ``shutil.rmtree(path, onerror=onerror)``
    """
    import stat
    if not os.access(path, os.W_OK):
        # Is the error an access error ?
        os.chmod(path, stat.S_IWUSR)
        func(path)
    else:
        raise



###############
# JSON RELATED
############### 

# Check JSON for correct keys presence
def checkJSON(data):
    print("=> Checking JSON for required keys")
    keys = ["savedCreds", "data"]
    for i in keys:
        if i not in data:
            print(Fore.RED+"Key","'{}'".format(i), "is not present")
            sys.exit(2)
    if data["savedCreds"] == "1":
        if "credentials" not in data:
            print(Fore.RED+"Key 'credentials' is needed when 'savedCreds' is 1")
            sys.exit(2)

# Read the JSON file
def readJSON(filename):
    # Read JSON from file
    with open(filename) as f:
        data = json.load(f)
        # print(data, type(data))
    print(Fore.GREEN + "=> JSON Data loaded successfully")
    return data

# Generate URL from username,repo-name and repo privacy
def createUrl(name,repoType):
    if repoType == "public":
        url = "https://github.com/{}/{}".format(username,name)
    elif repoType == "private":
        url = "https://{0}:{1}@github.com/{0}/{2}.git".format(username,password,name)
    else:
        raise ValueError
    return url

# Generate command from passed options
def createCommand(name, url, path):
    cmd = "git clone {0} {1}/{2} --depth=1".format(url, path, name)
    return cmd

# Populate username & password
def processCredentials(data):
    global username,password
    
    if data["savedCreds"] == "1":
        username = data['credentials']['username']
        password = data['credentials']['password']
    else:
        username = input("Username: ")
        password = getpass.getpass()

    username = urllib.parse.quote(username)
    password = urllib.parse.quote(password)



#############
# FEATURES
#############

# Clone the repositories
def clone(data, dir = None):
    if "data" not in data:
        print(Fore.RED + "data key missing")
        sys.exit(2)

    for item in data["data"]:
        # Create parent DIR
        if dir is None:
            pathlib.Path(item['path']).mkdir(parents=True, exist_ok=True)
        else:
            pathlib.Path(dir).joinpath(item['path']).mkdir(parents=True, exist_ok=True)

        url = createUrl(item['name'], item['type'])
        cmd = createCommand(item['name'], url, item['path'])
        
        print("")
        print(Fore.GREEN + "=> Cloning " + item['name'])
        print(Fore.CYAN+cmd)
        execCommandLive(cmd, dir)
    
    print("")
    print(Fore.GREEN + "=> All repositories have been cloned")
        
# Deletes All existing repository folders 
def clean(data):
    if "data" not in data:
        print(Fore.RED + "data key missing")
        raise KeyError
    
    print(Fore.GREEN+"=> Cleaning up all repositories...")
    for item in data["data"]:
        # Create parent DIR
        # print(item['path'])
        path = pathlib.Path(item['path']).joinpath(item['name'])
        # print(path)
        if path.exists():
            print("=> Removing: " + str(path))
            shutil.rmtree(path, ignore_errors=False, onerror=onerror)

# Check repositories for uncommited work
def status(data):
    if "data" not in data:
        print(Fore.RED + "data key missing")
        sys.exit(2)
    
    print(Fore.GREEN + "=> Checking repositories for uncommited work \n")

    for item in data["data"]:
        # Create parent DIR
        path = pathlib.Path(item['path']).joinpath(item['name'])
        
        # print("")
        print(Fore.GREEN + "• " + item['name'] + "  ", end="")
        process = subprocess.run("git status --porcelain=v2", cwd=str(path), capture_output=True)
        if process.stdout != b'':
            print("❌")
        else:
            print("✅")
    
    print("")
    # print(Fore.GREEN + "=> All repositories have been cloned")

# Sync up all repositories
def sync(data):
    if "data" not in data:
        print(Fore.RED + "data key missing")
        sys.exit(2)
    
    print(Fore.GREEN + "=> Syncing up repositories. This will do a pull & a push but doesn't handle any merge conflicts.")

    for item in data["data"]:
        # Create parent DIR
        path = pathlib.Path(item['path']).joinpath(item['name'])
        
        # print("")
        print(Fore.GREEN + "\n• " + item['name'] + "  ", end="\n")
        process1 = subprocess.run("git pull", cwd=str(path))
        process2 = subprocess.run("git push", cwd=str(path))
    
    print("")
    print(Fore.GREEN + "=> All repositories have been synced")

# List repositories managed by this tool
def listRepos(data):
    if "data" not in data:
        print(Fore.RED + "data key missing")
        sys.exit(2)
    
    print(Fore.GREEN + "=> List of Repositories\n")

    for item in data["data"]:
        # Create parent DIR
        path = pathlib.Path(item['path']).joinpath(item['name'])
        
        if path.exists():
            print(Fore.GREEN + "• Repo:      ",item['name'])
            print("  Location:  ", item['path'])
            # print("")        
    
    print("")

# Setup workspace with JSON passed as parameter
def setup(filename):
    print(Fore.CYAN +" Initializing Workspace")
    data = readJSON(filename)
    
    checkJSON(data)
    processCredentials(data)

    # Take workspace name from user input
    # foldername = input("Enter name of folder to setup workspace: ")
    foldername = "Workspace"
    workspacePath = pathlib.Path(foldername)

    # DEBUG: Delete the Workspace folder
    if workspacePath.exists():
        shutil.rmtree(workspacePath, ignore_errors=False, onerror=onerror)
    
    # Check if the folder already exists, if not create it else report error
    if workspacePath.exists():
        print(Fore.RED + "The folder {} already exists.".format(foldername))
        sys.exit(2)
    else:
        print("=> Creating folder {}".format(foldername))
        workspacePath.mkdir(parents=True, exist_ok=True)
    
    # Create hidden config directory .gitsync
    print("=> Creating hidden configuration directory .gitsync")
    Path(foldername).joinpath(".gitsync").mkdir(parents=True, exist_ok=True)
    
    # Copy JSON init file to config directory
    workspaceConfigPath = Path(foldername).joinpath(".gitsync")
    filePath = Path(filename)
    print("=> Copying JSON to workspace")
    shutil.copy(str(filePath), str(workspaceConfigPath))

    # Start the clones
    clone(data, workspacePath)


# Define Global Variables
username=""
password=""

# Print Github credentials being used
# print("=> Github Credentials:")
# print(Fore.BLUE + "Username: " + username)
# print(Fore.BLUE + "Password: " + password)

# clean(data)
# clone(data)
print(sys.argv)

# main function, execution starts here
def main():    

    if sys.argv[1] == "setup":
        if sys.argv.__len__ == 3:
            setup(sys.argv[2])
        else:
            print(Fore.RED + "Setup needs json file name as argument")
            sys.exit(3)
    
    data = readJSON(".gitsync/repos.json")
    
    checkJSON(data)
    processCredentials(data)

    if sys.argv[1] == "list":
        listRepos(data)
    elif sys.argv[1] == "status":
        status(data)
    elif sys.argv[1] == "pnp":
        sync(data)
    else:
        print("GitSync - A tool for keeping multiple git repositores under sync & organised")
        print("setup | list | status | pnp")
        print("setup - Setups the workspace using the JSON file")


# Start The Magic #
main()