#!/usr/bin/python
# main.py

import argparse
import logging
import sys

from twisted.internet import reactor

from controller import KeyboardController
from controller import MovementController
from event_manager import EventManager, BeginGameEvent
from game import Game
from network import begin_on_client_connect, connect_to_server_host
from utils import apply_fn


WIDTH = 480
HEIGHT = 480
IS_HOST = None
HOST = None
PORT = None
logging.basicConfig(level=logging.DEBUG)


def parse_args():
    global IS_HOST
    global HOST
    global PORT
    parser = argparse.ArgumentParser(description='PyTron: The Tasty Tron')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--host',
        metavar='PORT',
        type=int,
        help='Run as host for multiplayer',
    )
    group.add_argument(
        '--client',
        metavar='HOSTNAME:PORT',
        help='Run as client for multiplayer',
    )
    args = parser.parse_args(sys.argv[1:])
    if args.host:
        HOST, PORT = 'localhost', int(args.host)
        IS_HOST = True
    elif args.client:
        HOST, PORT = args.client.split(':')
        PORT = int(PORT)
        IS_HOST = False
    logging.info('Setting host to {h}:{p}'.format(h=HOST, p=PORT))


def main():
    # parse_args()
    ev = EventManager()
    game = Game(ev, WIDTH, HEIGHT)
    keybd = KeyboardController(ev)
    movement_controller = MovementController(ev, game.sprites, game.board)
    apply_fn(
        lambda x: ev.register_listener(x),
        [
            keybd,
            game,
            movement_controller,
        ],
    )
    ev.post(BeginGameEvent())
    # if IS_HOST:
        # begin_on_client_connect(ev, PORT)
    # else:
        # connect_to_server_host(ev, HOST, PORT)

    reactor.run()

main()
