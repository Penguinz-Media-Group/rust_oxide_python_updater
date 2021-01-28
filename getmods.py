from requests import get
from os import path
from helper import RustHelper

rh = RustHelper()
logger = rh.logger(functionname="getmods")

class LoadMod:
    def __init__(self):
        self.pluginconf = "plugins.json"
        self.cnf = rh.loadconf(self.pluginconf)


    def pull_mod(self, url, oxidefile):
        # TODO convert this to generic pull file
        file = rh.pullwebfile(url)
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


    def install_dll(self, url, filename="Oxide.Ext.RustIO.dll"):

        try:
            file = rh.pullwebfile(url)
        except Exception as err:
            print("Error retrieving dll file: %s" % err)
        oxidefile = str(path.abspath("/opt/rust/RustDedicated_Data/Managed/" + filename))
        try:
            with open(oxidefile, 'w') as oxide:
                oxide.write(file.content)
                oxide.close()
        except Exception as err:
            logger.error("Error writing to file: %s" % err)


if __name__ == "__main__":
    x = LoadMod()
    x.load_conf()
    if "communitybundle" in x.cnf:
        x.install_dll("http://playrust.io/latest")
    x.bundle_checker()



