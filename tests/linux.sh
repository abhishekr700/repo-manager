#!/bin/bash

PYTHON=python3
echo "==> Removing Workspace if present"
rm -rf Workspace
echo "==> Setting up Workspace"
$PYTHON repomgr.py setup sample.json
echo "==> Moving to Workspace"
cd Workspace
echo "==> Syncing Up"
$PYTHON ../repomgr.py sync
echo "==> Removing Something"
rm -rf 03CPP-Stuff
echo "==> Sync Again"
$PYTHON ../repomgr.py sync
echo "==> Listing"
$PYTHON ../repomgr.py list
echo "==> CleanAll & CloneAll"
$PYTHON ../repomgr.py cnc
echo "==> Status"
$PYTHON ../repomgr.py status
echo "==> Status with a cross"
echo "Boooooooooo" > 03CPP-Stuff/01Projects/Chat-Server-Client/a.txt
$PYTHON ../repomgr.py status
rm -rf 03CPP-Stuff\01Projects\Chat-Server-Client\a.txt
cd ../
