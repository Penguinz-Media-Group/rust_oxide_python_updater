#!/usr/bin/python3

import json
from requests import get


# https://github.com/OxideMod/Oxide.Rust/releases/download/2.0.4882/Oxide.Rust-linux.zip
# url = "https://github.com/OxideMod/Oxide.Rust/releases/latest/download/Oxide.Rust-linux.zip"


versionfile = "version.json"
oxidezip = "oxide.zip"
oxidedir = "."


def getoxideversion():
    versionurl = "https://umod.org/games/rust/latest.json"
    try:
        page = get(versionurl)
    except Exception as err:
        print("Error retrieving version file: %s" % err)
    content = page.content
    data = json.loads(content.decode())

    version = (data["version"])
    return version


def getinstalledversion():

    try:
        with open(versionfile, 'r') as vfile:
            x = vfile.readline()
            y = json.loads(x)['version']
            vfile.close()
    except Exception as err:
        print(err)
        y = "0"
    return y


def updateoxide(version, oxidefile):
    jsonout = {}
    downloadurl = ["https://github.com/OxideMod/Oxide.Rust/releases/download/", "/Oxide.Rust-linux.zip"]
    jsonout['version'] = version
    print("Updating")
    url = downloadurl[0] + version + downloadurl[1]
    try:
        file = get(url, allow_redirects=True)
    except Exception as err:
        print("Error retrieving oxide file: %s" % err)
    try:
        with open(oxidefile, 'wb') as oxide:
            oxide.write(file.content)
            oxide.close()
        with open(versionfile, 'w') as vfile:
            json.dump(jsonout, vfile)
            vfile.close()
    except Exception as err:
        print("Error writing to file: %s" % err)

def unzipfile(zipfile, zipdir,mode='r'):
    from os import remove
    try:
        from zipfile import ZipFile
        with ZipFile(zipfile, 'r') as zp:
            zp.extractall(zipdir)
    except Exception as err:
        print("Failed to unzip oxide package: %s" % err)
        return False
    if mode == "r":
        try:
            remove(zipfile)
        except Exception as err:
            print("Failed to cleanup oxide package: %s" % err)
            return False
    return True

curversion = getoxideversion()
instversion = getinstalledversion()
if curversion > instversion:
    updateoxide(curversion, oxidezip)
    unzipfile(oxidezip, oxidedir)

else:
    print("Latest Version")
