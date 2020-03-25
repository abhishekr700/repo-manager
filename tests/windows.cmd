@echo off
echo "==> Removing Workspace if present"
rmdir /S /Q Workspace
echo "==> Setting up Workspace"
python repomgr.py setup repos.json
echo "==> Moving to Workspace"
cd Workspace
echo "==> Syncing Up"
python ../repomgr.py sync
echo "==> Removing Something"
rmdir /S /Q 03CPP-Stuff
echo "==> Sync Again"
python ../repomgr.py sync
echo "==> Listing"
python ../repomgr.py list
echo "==> CleanAll & CloneAll"
python ../repomgr.py cnc
echo "==> Status"
python ../repomgr.py status
echo "==> Status with a cross"
echo "Boooooooooo" > 03CPP-Stuff/01Projects/Chat-Server-Client/a.txt
python ../repomgr.py status
DEL 03CPP-Stuff\01Projects\Chat-Server-Client\a.txt
cd ../