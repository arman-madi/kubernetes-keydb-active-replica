# keydb-stream-consumer
#
# Created on 25-01-2021
#
# Author
#   Arman (https://www.linkedin.com/in/armanmadi/)
#
# Description:
#   This script demonstrates how to consume a KeyDB stream

from datetime import datetime
from os import environ

import redis


def process_message(msg_id, message):
    print(f'Processing message ({msg_id}:{message})')


def main():
    name = environ['HOSTNAME']
    print(f"{datetime.now().time()} - Consumer {name} starting...")
    stream_name = "stream1"
    group_name = "A"
    # Using defined service name in components.yaml to connect to one of the keydb replicas
    r = redis.Redis(host='keydb')
    last_processed_id = 0
    check_backlog = True
    while True:
        """ 
            Pick the ID based on the iteration: the first time we want to
            read our pending messages, in case we crashed and are recovering.
            Once we consumed our history, we can start getting new messages.
        """
        start_id = last_processed_id if check_backlog else '>'

        print(f"{datetime.now().time()} - *** XREADGROUP ***")
        items = r.xreadgroup(group_name,
                             name,
                             {stream_name: start_id},
                             10,
                             2000
                             )

        if items is None or len(items) == 0:
            print("Timeout!")
            continue
        if len(items[0]) != 2 or type(items[0][1]) is not list:
            print(f"{datetime.now().time()} - Unexpected items format!")
            print(items)
            continue
        # If we receive an empty reply, it means we were consuming our history
        # and that the history is now empty. Let's start to consume new messages.
        check_backlog = False if len(items[0][1]) == 0 else check_backlog

        for message in items[0][1]:
            msg_id = message[0]
            # Process the message
            process_message(msg_id, message[1])

            # Acknowledge the message as processed
            r.xack(stream_name, group_name, msg_id)
            last_processed_id = msg_id


if __name__ == '__main__':
    main()

