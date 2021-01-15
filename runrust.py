#!/usr/bin/python3
from  subprocess import run
import json
from sys import exit

rustpw = "rustpw.json"
rustconf = "rust.conf"

# TODO add premium support for getopts
def getpw():
    try:
        with open(rustpw, 'r') as pwf:
            pw = pwf.readline()
            pw = json.loads(pw)['password']
            pwf.close()
    except Exception as err:
        print("Unable to read pw, quiting!")
        exit(1)
    return pw

def runserver(pw):
    from updaterust import UpdateServer
    x = UpdateServer
    conf = x.loadconf()
    # TODO add premium conf loading for id, map, save interval, global chat, and removal of PMG desc add
    opts = '-batchmode -nographics  -rcon.ip %s -rcon.port %s -rcon.password %s -server.ip %s ' \
           '-server.port %s -server.maxplayers %s -server.hostname %s -server.identity "ServerByPMG" -server.seed %s' \
           '-server.level "Procedural Map" -server.worldsize %s -server.saveinterval 3600 -server.globalchat true ' \
           '-server.description %s -server.headerimage %s -server.url %s'  % \
           (conf['ip'], conf['rport'], pw, conf['ip'],  conf['sport'], conf['players'], conf['hostname'], conf['seed'],
            conf['worldsize'], conf['desc'] + pmgdesc, conf['image'], conf['url'] )
    try:
        if conf['logfile']:
            log = open(conf['logfile'], 'w')
        else:
            log = open("rust.log", 'w')
    except Exception as err:
        print('Unable to write to log file')
    try:
        run(['RustDedicated', opts], stdout=log)
    except Exception as err:
        print("Unable to start Rust Server!")
        return
    print("Starting Rust Server with PMG assistance!")

pw = getpw()
runserver(pw)





pmgdesc = "\n A PMG assisted server. https://penguinzmedia.group/rust"