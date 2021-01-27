# keydb-stream-producer
#
# Created on 25-01-2021
#
# Author
#   Arman (https://www.linkedin.com/in/armanmadi/)
#
# Description:
#   This script demonstrates how to produce messages for a KeyDB stream

from datetime import datetime
from os import environ
from random import randrange, random
from time import sleep

import redis


def main():
    name = environ['HOSTNAME']
    print(f"{datetime.now().time()} - Producer {name} starting...")
    stream_key = "stream1"
    group_name = "A"
    veh_flag = ['maintenance', 'transfer', 'available', 'standby', 'service']
    # Using defined service name in components.yaml to connect to one of the keydb replicas
    r = redis.Redis(host='keydb')
    r.xgroup_create(stream_key, group_name, 0, True)
    while True:
        msg = {"vehicle_id": randrange(1000), "status": veh_flag[randrange(5)]}
        r.xadd(stream_key, msg)
        print(f'{datetime.now().time()} - message added: {msg}')
        sleep(random()*3+0.5)


if __name__ == '__main__':
    main()

