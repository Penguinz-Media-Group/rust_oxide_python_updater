#!/usr/bin/python3

import json
from helper import RustHelper
import sys

rh = RustHelper()
logger = rh.logger(functionname="updaterust")

class UpdateServer:

    def __init__(self, args):
        self.versionfile = "version.json"
        self.oxidezip = "oxide.zip"
        self.oxidedir = "."
        self.rustconf = "rustconf.json"
        self.conf = {}
        self.conf = rh.loadconf(self.rustconf)
        self.conf.update(rh.parseopts(args))
        self.versionurl = "https://umod.org/games/rust/latest.json"

    def getoxideversion(self):
        content = rh.pullwebfile(self.versionurl)
        data = json.loads(content.decode())
        version = (data["version"])
        logger.debug("Latest Oxide Version: %s" % version)
        return version

    def getinstalledversion(self):
        try:
            x = rh.loadconf(self.versionfile)
            y = json.loads(x)['version']
        except Exception as err:
            logger.error(err)
            y = "0"
        logger.debug('Current Install Oxide Version')
        return y


    def updateoxide(self, version, oxidefile):
        jsonout = {}
        downloadurl = ["https://github.com/OxideMod/Oxide.Rust/releases/download/", "/Oxide.Rust-linux.zip"]
        jsonout['version'] = version
        print("Updating")
        url = downloadurl[0] + version + downloadurl[1]
        logger.debug("Download URL: %s" % url)
        file = rh.pullwebfile(url)
        try:
            with open(oxidefile, 'wb') as oxide:
                oxide.write(file.content)
                oxide.close()
            with open(self.versionfile, 'w') as vfile:
                json.dump(jsonout, vfile)
                vfile.close()
        except Exception as err:
            logger.error("Error writing to file: %s" % err)



    def updateserver(self):
        pass


    def runrustupdate(self):
        self.updateserver()
        logger.debug(self.conf)
        if self.conf['modded'] == "1":
            curversion = self.getoxideversion()
            instversion = self.getinstalledversion()
            if curversion > instversion:
                self.updateoxide(curversion, self.oxidezip)
                rh.unzipfile(self.oxidezip, self.oxidedir)
            else:
                logger.info("Latest Version")
        logger.info("Rust is up to date!")


if __name__ == "__main__":
    x = UpdateServer(sys.argv)
    x.runrustupdate()