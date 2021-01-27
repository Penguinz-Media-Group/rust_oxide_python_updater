from requests import get
from os import path
import json
import logging
import sys

logging.basicConfig(filename="rust.log", level=logging.DEBUG)
logger = logging.getLogger('oxideplugininstall')

sys.stdout.write = logger.info
sys.stderr.write = logger.error


class loadmod:
    def __init__(self):
        self.pluginconf = "plugins.json"
        self.cnf = {}

    def load_conf(self):
        # TODO add premium remote package pull via rest
        # TODO pull common functions into a single library
        try:
            with open(self.pluginconf, 'r') as cnf:
                conf = cnf.readlines()
                conf = ''.join(conf)
                conf = json.loads(conf)
                logger.debug("Read in configuration for  Oxide Plugins.")
        except Exception as err:
            logger.error("Unable to load config file!")
        self.cnf = conf


    def pull_mod(self, url, oxidefile):
        # TODO convert this to generic pull file
        try:
            file = get(url, allow_redirects=True)
        except Exception as err:
            print("Error retrieving oxide file: %s" % err)
        oxidefile = str(path.abspath("/opt/rust/oxide/plugins/" + oxidefile))
        try:
            with open(oxidefile, 'w') as oxide:
                oxide.write(file.content)
                oxide.close()
        except Exception as err:
            logger.error("Error writing to file: %s" % err)


    def bundle_installer(self, bundle):
        for name, url in bundle.items():
            logger.debug("Installing  mod %s" % name)
            try:
                self.pull_mod(url, name + ".cs")
            except Exception as err:
                logger.error("Failed to pull mod file %s due to %s" % (name, err) )


    def bundle_checker(self):
        print("Bundle Check")
        for name, state in self.cnf['enabled'].items():
            if state == "true":
                logger.info("Installing bundle %s" % name)
                self.bundle_installer(self.cnf[name])


    def install_dll(self, url):
        # TODO Migrate to a single file pull / installer
        try:
            file = get(url, allow_redirects=True)
        except Exception as err:
            print("Error retrieving dll file: %s" % err)
        oxidefile = str(path.abspath("/opt/rust/RustDedicated_Data/Managed/" + oxidefile))
        try:
            with open(oxidefile, 'w') as oxide:
                oxide.write(file.content)
                oxide.close()
        except Exception as err:
            logger.error("Error writing to file: %s" % err)


if __name__ == "__main__":
    x = loadmod()
    x.load_conf()
    if "communitybundle" in x.cnf:
        x.install_dll("http://playrust.io/latest")
    x.bundle_checker()



