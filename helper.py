import json
from requests import get


class RustHelper:

    def __init__(self):
        pass

    def loadconf(self, path, source="json"):
        if source == "json":
            try:
                with open(path, 'r') as cnf:
                    conf = cnf.readlines()
                    conf = ''.join(conf)
                    conf = json.loads(conf)
            except Exception as err:
                logger.error("Unable to load configuration: %s" % err)
        elif source == "ini":
            from configparser import SafeConfigParser
            try:
                config = SafeConfigParser
                with open(path, 'r') as cnf:
                    conf = config.read(cnf)
            except Exception as err:
                logger.error("Unable to load configuration: %s" % err)
        elif source == "api":
            logger.critical("This is not a premium script! Please contact PMG for premium license!")
        else:
            logger.error("Invalid config options passed!")
        return conf

    def parseopts(self, args):
        import getopt
        conf = {}
        try:
            opts, args = getopt.getopt(args, "hm:v", ["help", "mode="])
            for o, a in opts:
                if o == "-v":
                    print("Version 3.X")
                elif o in ("-m", "--mode"):
                    conf['mode'] == a
                elif o in ("-h", "--help"):
                    print("Help:")
                    print("-m --mode=    <mode>")
                    print("modes: docker, native")
        except Exception as err:
            logger.error("Unable to get options: %s" % err)
        return conf


    def pullwebfile(self, url, auth={}, redirects=True):
        try:
            if len(auth) > 1:
                page = get(url, allow_redirects=redirects, auth=auth)
            else:
                page = get(url,  allow_redirects=redirects)
            content = page.content
        except Exception as err:
            logger.error("Error retrieving version file: %s" % err)
            return
        return content

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

    def logger(self, output="file", logfile="rust.log", functionname="rustmanager"):
        import logging
        import sys
        if output == "file":
            logging.basicConfig(filename=logfile, level=logging.DEBUG)
        elif output == "stdout":
            logging.basicConfig(level=logging.DEBUG)
        log = logging.getLogger(functionname)
        sys.stdout.write = log.info
        sys.stderr.write = log.error
        return log


rh = RustHelper()
logger = rh.logger(functionname="RustHelper")
