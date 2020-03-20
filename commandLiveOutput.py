import subprocess, sys
import shlex

# invoke process
# process = subprocess.Popen(shlex.split("git clone https://github.com/ccxt/ccxt"),shell=False,stdout=subprocess.PIPE)

# # Poll process.stdout to show stdout live
# while True:
#   output = process.stdout.readline()
#   if process.poll() is not None:
#     break
#   if output:
#     print (output.strip())
# rc = process.poll()

def execCommandLive(cmd, dir = None):
    print("Exec Command: ",cmd,dir)
    if dir is None:
        process = subprocess.Popen(shlex.split(cmd),shell=False,stdout=subprocess.PIPE)
    else:
        process = subprocess.Popen(shlex.split(cmd),shell=True,stdout=subprocess.PIPE, cwd=dir)

    all = ""
    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip())
            # print("2OUT:", output)
            all+=str(output.strip())
        rc = process.poll()

    print("ALL: ",process)