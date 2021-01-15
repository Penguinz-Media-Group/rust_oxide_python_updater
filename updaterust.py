#!/usr/bin/python3

import json
from requests import get
import logging

FORMAT = '%(asctime)-15s %(function)-8s %(message)s'
logging.basicConfig(filename="rust.log", level=logging.DEBUG)
logger = logging.getLogger('rustserver')

class UpdateServer:

    def __init__(self):
        self.versionfile = "version.json"
        self.oxidezip = "oxide.zip"
        self.oxidedir = "."
        self.rustconf = "rustconf.json"
        self.conf = {}

    def getoxideversion(self):
        versionurl = "https://umod.org/games/rust/latest.json"
        try:
            page = get(versionurl)
        except Exception as err:
            logger.error("Error retrieving version file: %s" % err)
        content = page.content
        data = json.loads(content.decode())

        version = (data["version"])
        logger.debug("Latest Oxide Version: %s" % version)
        return version


    def getinstalledversion(self):

        try:
            with open(self.versionfile, 'r') as vfile:
                x = vfile.readline()
                y = json.loads(x)['version']
                vfile.close()
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
        try:
            file = get(url, allow_redirects=True)
        except Exception as err:
            print("Error retrieving oxide file: %s" % err)
        try:
            with open(oxidefile, 'wb') as oxide:
                oxide.write(file.content)
                oxide.close()
            with open(self.versionfile, 'w') as vfile:
                json.dump(jsonout, vfile)
                vfile.close()
        except Exception as err:
            logger.error("Error writing to file: %s" % err)

    def unzipfile(self, zipfile, zipdir,mode='r'):
        from os import remove
        try:
            from zipfile import ZipFile
            with ZipFile(zipfile, 'r') as zp:
                zp.extractall(zipdir)
        except Exception as err:
            logger.error("Failed to unzip oxide package: %s" % err)
            return False
        if mode == "r":
            try:
                remove(zipfile)
            except Exception as err:
                logger.warning("Failed to cleanup oxide package: %s" % err)
                return False
        return True

    def updateserver(self):
        from subprocess import Popen
        from io import StringIO
        try:
            if self.conf['logfile']:
                log = open(self.conf['logfile'], 'w')
            else:
                log = open("rust.log", 'w')
        except Exception as err:
            logger.warning('Unable to write to log file')
        try:
            Popen(["/usr/games/steamcmd", " +login anonymous +force_install_dir . +app_update 258550  validate"],
                stdout=logger.info)
            output, error = process.communicate()
            logger.error(StringIO(error))
            logger.info(StringIO(output))
        except Exception as err:
            logger.error("Error while updating steam: %s" % err)

    def loadconf(self):
        import string
        # TODO add premium remote package pull
        try:
            with open(self.rustconf, 'r') as cnf:
                self.conf = cnf.readlines()
                self.conf = ''.join(self.conf)
                self.conf = json.loads(self.conf)
        except Exception as err:
            logger.error("Unabel to load config file!")

    def runrustupdate(self):
        self.loadconf()
        self.updateserver()
        logger.debug(self.conf)
        if self.conf['modded'] == "1":
            curversion = self.getoxideversion()
            instversion = self.getinstalledversion()
            if curversion > instversion:
                self.updateoxide(curversion, self.oxidezip)
                self.unzipfile(self.oxidezip, self.oxidedir)
            else:
                logger.info("Latest Version")
        logger.info("Rust is up to date!")

if __name__ == "__main__":
    x = UpdateServer()
    x.runrustupdate()