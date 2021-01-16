#!/usr/bin/python3

import json
from requests import get
import logging
import sys

logging.basicConfig(filename="rust.log", level=logging.DEBUG)
logger = logging.getLogger('rustserverupdate')

sys.stdout.write = logger.info
sys.stderr.write = logger.error

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
        import subprocess
        # from io import StringIO
        try:
            logger.debug("Running steam update")
            subprocess.Popen(["/usr/games/steamcmd", " +login anonymous +force_install_dir . "
                                                               "+app_update 258550  validate"])
            '''  Will come back to this at some point. Would like to be able to log this out rather than stdout.
            process = subprocess.Popen(
            #    ["/usr/games/steamcmd", " +login anonymous +force_install_dir . +app_update 258550  validate"],
            #    stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            while True:
                output = process.stdout.readline()
                error = process.stderr.readline()
                if output == '' and process.poll() is not None:
                    break
                if output:
                    logger.info(StringIO(output))
                if error == '' and process.poll() is not None:
                    break
                if error:
                    logger.error(StringIO(error))
            rc = process.poll() **/ '''
        except Exception as err:
            logger.error("Error while updating steam: %s" % err)

    def loadconf(self):
        # TODO add premium remote package pull
        try:
            with open(self.rustconf, 'r') as cnf:
                self.conf = cnf.readlines()
                self.conf = ''.join(self.conf)
                self.conf = json.loads(self.conf)
                logger.debug("Read in configuration for rust / oxide update.")
        except Exception as err:
            logger.error("Unable to load config file!")

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