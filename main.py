#!/usr/bin/python
# main.py

import argparse
import sys

from twisted.internet import reactor

from controller import KeyboardController
from controller import MovementController
from event_manager import EventManager
from game import Game
from network import begin_on_client_connect
from utils import apply_fn


WIDTH = 480
HEIGHT = 480
HOST = None
PORT = None


def parse_args():
    global HOST
    global PORT
    parser = argparse.ArgumentParser(description='PyTron: The Tasty Tron')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        '--host',
        metavar='PORT',
        help='Run as host for multiplayer',
    )
    group.add_argument(
        '--client',
        metavar='HOSTNAME:PORT',
        help='Run as client for multiplayer',
    )
    args = parser.parse_args(sys.argv[1:])
    if args.host:
        HOST = 'localhost'
        PORT = args.host
    elif args.client:
        HOST, PORT = args.client.split(':')


def main():
    parse_args()

main()
