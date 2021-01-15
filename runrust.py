#!/usr/bin/python3
from  subprocess import run
import json
from os import exit

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
    # TODO add premium remote package pull
    with open(rustconf, 'r') as cnf:
        conf = cnf.readlines()
        conf = json.loads(conf.decode())
    # TODO add premium conf loading for id, map, save interval, global chat, and removal of PMG desc add
    opts = '-batchmode -nographics  -rcon.ip %s -rcon.port %s -rcon.password %s -server.ip %s ' \
           '-server.port %s -server.maxplayers %s -server.hostname %s -server.identity "ServerByPMG" -server.seed %s' \
           '-server.level "Procedural Map" -server.worldsize %s -server.saveinterval 3600 -server.globalchat true ' \
           '-server.description %s -server.headerimage %s -server.url %s'  % \
           (conf['ip'], conf['rport'], pw, conf['ip'],  conf['sport'], conf['players'], conf['hostname'], conf['seed'],
            conf['worldsize'], conf['desc'] + pmgdesc, conf['image'], conf['url'] )
    try:
        run(['RustDedicated', opts])
    except Exception as err:
        print("Unable to start Rust Server!")
        return
    print("Starting Rust Server with PMG assistance!")

pw = getpw()
runserver(pw)





pmgdesc = "\n A PMG assisted server. https://penguinzmedia.group/rust"