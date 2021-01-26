from requests import get
from os import path
import json
import logging
import sys

logging.basicConfig(filename="rust.log", level=logging.DEBUG)
logger = logging.getLogger('oxideplugininstall')

sys.stdout.write = logger.info
sys.stderr.write = logger.error


def load_conf(pluginconf):
    # TODO add premium remote package pull via rest
    # TODO pull common functions into a single library
    try:
        with open(pluginconf, 'r') as cnf:
            conf = cnf.readlines()
            conf = ''.join(conf)
            conf = json.loads(conf)
            logger.debug("Read in configuration for  Oxide Plugins.")
    except Exception as err:
        logger.error("Unable to load config file!")


def pull_mod(url, oxidefile,  zipped):
    try:
        file = get(url, allow_redirects=True)
    except Exception as err:
        print("Error retrieving oxide file: %s" % err)
    oxidefile = path.abspath("/opt/rust/oxide/plugins" + oxidefile)
    try:
        with open(oxidefile, 'wb') as oxide:
            oxide.write(file.content)
            oxide.close()
    except Exception as err:
        logger.error("Error writing to file: %s" % err)


def unzipfile(zipfile, zipdir,mode='r'):
    from os import remove
    from zipfile import ZipFile
    try:
        with ZipFile(zipfile, 'r') as zp:
            zp.extractall(zipdir)
    except Exception as err:
        logger.error("Failed to unzip package: %s" % err)
        return False
    if mode == "r":
        try:
            remove(zipfile)
        except Exception as err:
            logger.warning("Failed to cleanup package: %s" % err)
            return False
    return True

pluginconf = "plugins.json"
