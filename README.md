# Repo Manager 👋

![Version](https://img.shields.io/badge/version-1.0-blue.svg?cacheSeconds=2592000)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/abhishekr700/repo-manager/blob/master/LICENSE)

> A cross-patform tool for managing & syncing multiple git repositories while simultaneously keeping them arranged in a user defined directory hierarchy.

## Why ?

I have a few private repositories where I keep some code snippets as well as some project repositories I often look for while coding.Therefore I need to clone them on every laptop/pc I work on.To achieve this I had to clone and sync up each individual repo on each individual machine whenever some update was there to one or more repos. When looking at the tools, I found the tool `repo` by google which unfortunately was not natively supported for Windows. Thus, I started this little python script for the same, which turned out to be quite helpful, I made it a little more user friendly and released it as a mini project.

## Requirements

Python 3.6+

## Install

1. `git clone https://github.com/abhishekr700/repo-manager`
2. `cd repo-manager`
3. `pip install -r requirements.txt`
4. Edit the JSON file according to the format shown below
5. Windows
    > Clone this repository and use it like `python3 repomgr.py [args]`

    Linux (Tested on Ubuntu)

    ```sh
    ./install_linux.sh
    ```

## Usage

1. You need to first initialize your Workspace by running `repomgr setup /pat/to/jsonfile`
2. After this your workspace will be set up.
3. Go into the workspace and try the commands shown below.

```text
Usage: python test.py setup | list | status | sync | cnc

setup - Setups the workspace using the JSON file
list - List the repositories managed by this tool
status - Check for uncommited work in the repositories
sync - Goto each repository and do a git pull followed by a git push
cnc - Clean & re-clone all repositories
help - Print this help
```

## JSON Format

The whole file is a JSON Object.

- savedCreds: '0' if you want to specify credentials everytime you run the script. '1' if you want to save the credentials. if '1', you need to specify the key 'credentials'

- credentials: Git Credentials to use
  - credentials.username: Github Username
  - credentials.password: Github Password

- data: An array of Objects, each one specifying a repository
  - Repository Format
    
    ```js
    {
        "name": "OnlineAuction", //Name of repository
        "type": "public",   // private or public
        "path": "01WebProjects" // Location to clone to
    }
    ```

> For more clarity regarding this file, check `sample.json` file

## Run tests

Windows

```sh
./tests/windows.cmd
```

Linux

```sh
./tests/linux.sh
```

## Author

👤 **Abhishek Ranjan**

* Github: [@abhishekr700](https://github.com/abhishekr700)

## 🤝 Contributing

Contributions, issues and feature requests are welcome!

Feel free to check [issues page](https://github.com/abhishekr700/repo-manager/issues). 

## Show your support

Give a ⭐️ if this project helped you!


## 📝 License

Copyright © 2020 [Abhishek Ranjan](https://github.com/abhishekr700).

This project is [GNU GPL V3.0](https://github.com/abhishekr700/repo-manager/blob/master/LICENSE) licensed.
