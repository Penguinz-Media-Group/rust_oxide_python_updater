#!/usr/bin/python3
import subprocess
import json
from sys import exit
import logging

rustpw = "rustpw.json"
rustconf = "rustconf.json"


FORMAT = '%(asctime)-15s  %(function)-8s %(message)s'
logging.basicConfig(filename="rust.log", level=logging.DEBUG)
logger = logging.getLogger('rustserverexec')



# TODO add premium support for getopts
def getpw():
    try:
        with open(rustpw, 'r') as pwf:
            pw = pwf.readline()
            pw = json.loads(pw)['password']
            pwf.close()
    except Exception as err:
        logger.error("Unable to read pw, quiting!")
        exit(1)
    return pw

def loadconf():
    # TODO add premium remote package pull
    try:
        with open(rustconf, 'r') as cnf:
            conf = cnf.readlines()
            conf = ''.join(conf)
            conf = json.loads(conf)
    except Exception as err:
        logger.error("Unable to load configuration: %s" % err)
    return conf

def runserver(pw):
    from io import StringIO

    conf = loadconf()
    pmgdesc = "\n A PMG assisted server. https://penguinzmedia.group/rust"
    logger.info('Starting Rust Server')
    # TODO add premium conf loading for id, map, save interval, global chat, and removal of PMG desc add
    opts = '-batchmode -nographics  -rcon.ip %s -rcon.port %s -rcon.password %s -server.ip %s ' \
           '-server.port %s -server.maxplayers %s -server.hostname %s -server.identity "ServerByPMG" -server.seed %s' \
           '-server.level "Procedural Map" -server.worldsize %s -server.saveinterval 3600 -server.globalchat true ' \
           '-server.description %s -server.headerimage %s -server.url %s'  % \
           (conf['ip'], conf['rport'], pw, conf['ip'],  conf['sport'], conf['players'], conf['hostname'], conf['seed'],
            conf['worldsize'], conf['desc'] + pmgdesc, conf['image'], conf['url'] )

    try:
        process = subprocess.Popen(['RustDedicated', opts], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output, error = process.communicate()
        logger.error(StringIO(error))
        logger.info(StringIO(output))
    except Exception as err:
        logger.error("Unable to start Rust Server: %s" % err)
        return
    logger.info("Starting Rust Server with PMG assistance!")

pw = getpw()
runserver(pw)





