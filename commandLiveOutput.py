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

def execCommand(cmd):
    process = subprocess.Popen(shlex.split(cmd),shell=False,stdout=subprocess.PIPE)

    # Poll process.stdout to show stdout live
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip())
        rc = process.poll()