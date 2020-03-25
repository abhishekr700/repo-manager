#!/bin/bash
echo "=== Repo Manager Install ===" 
echo "=> Installing dependencies"
pip3 install -r requirements.txt
echo "=> Making repomgy.py executable"
chmod +x repomgr.py
echo "=> Copying files to /usr/bin"
cp repomgr.py /usr/bin/repomgr
cp commandLiveOutput.py /usr/bin/
echo "=> Done ! Reload your shell"