#!/usr/bin/python3
# Test RCON connection based on a file list of ports

import rcon as r


def test_alive(port, password):
    alive = run_rcon(port=port, command="uptime", password=password)
    if len(alive) > 1:
        return True
    else:
        return False


def run_rcon(port, command, password,  args="", ip="127.0.0.1"):
    try:
        response = await r.rcon(command, args, host=ip, port=port, passwd=password)
    except Exception as err:
        print(err)
        response = ""
    return response
