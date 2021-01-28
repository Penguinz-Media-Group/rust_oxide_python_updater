#!/usr/bin/python3
import subprocess
import json
from helper import RustHelper
import sys

rh = RustHelper()
logger = rh.logger(functionname="runrust")


class RunRust:

    def __init__(self, arg):
        self.conf = {}
        self.rustpw = "rustpw.json"
        self.rustconf = "rustconf.json"
        self.conf = rh.loadconf(self.rustconf)
        self.conf.update(rh.parseopts(arg))
        self.pw = self.getpw()

    def getpw(self):
        try:
            pw = rh.loadconf(self.rustpw)
            pw = json.loads(pw)['password']
        except Exception as err:
            logger.error("Using default password due to error reading password: %s" % err)
            pw = "ChangeMe"
        return pw

    def runserver(self, pw=""):
        if len(pw) < 2:
            pw = self.pw
        conf = self.conf  # laziness maybe, but I dont want to rewrite all of this yet when I know I will have to later
        pmgdesc = "\n A PMG assisted server. https://penguinzmedia.group/rust"
        logger.info('Starting Rust Server')
        logger.debug(conf)
        # TODO add premium conf loading for id, map, save interval, global chat, and removal of PMG desc add
        opts = '-batchmode -nographics  -rcon.ip "%s" -rcon.port "%s" -rcon.password "%s" -server.ip "%s" ' \
               '-server.port "%s" -server.maxplayers "%s" -server.hostname "%s" -server.identity "ServerByPMG" ' \
               '-server.seed "%s" -server.level "Procedural Map"' \
               '-server.worldsize "%s" -server.saveinterval "3600" -server.globalchat "true" ' \
               '-server.description "%s" -server.headerimage "%s" -server.url "%s"' % \
               (conf['ip'], conf['rport'], pw, conf['ip'],  conf['sport'], conf['players'], conf['hostname'],
                conf['seed'], conf['worldsize'], conf['desc'] + pmgdesc, conf['image'], conf['url'])
        logger.debug("%s" % opts)

        try:
            subprocess.run(['/opt/rust/RustDedicated', opts])
        except Exception as err:
            logger.error("Unable to start Rust Server: %s" % err)
            return
        logger.info("Starting Rust Server with PMG assistance!")


x = RunRust(sys.argv)
x.runserver()
