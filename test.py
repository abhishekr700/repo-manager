
username=""
password=""

from commandLiveOutput import execCommand

# Generate URL from username,repo-name and repo privacy
def createUrl(name,repoType):
    if repoType == "public":
        url = "https://github.com/{}/{}".format(username,name)
    elif repoType == "private":
        url = "https://{0}:{1}@github.com/{0}/{2}.git".format(username,password,name)
    else:
        raise ValueError
    return url

def createCommand(name, url, path):
    cmd = "git clone {0} {1}/{2}".format(url, path, name)
    return cmd


# Module needed
import json
import pathlib
import urllib

username = urllib.parse.quote(username)
password = urllib.parse.quote(password)


# Read JSON from file
with open("repos.json") as f:
    data = json.load(f)
    # print(data, type(data))

data = data['data']

for item in data:
    # print(item, type(item))
    # print(createUrl(item['name'], item['type']))
    # Create parent DIR
    pathlib.Path(item['path']).mkdir(parents=True, exist_ok=True)
    url = createUrl(item['name'], item['type'])
    cmd = createCommand(item['name'], url, item['path'])
    execCommand(cmd)
    print(cmd)
    



# print(data, type(data))

# Pretty Print JSON
# print(json.dumps(data,indent=4))