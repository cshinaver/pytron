#!/usr/bin/python
# main.py

from view import View
from game import Game
from event_manager import EventManager
from controller import KeyboardController
from utils import apply_fn


WIDTH = 340
HEIGHT = 480


def main():
    ev = EventManager()
    game = Game(ev)
    keybd = KeyboardController(ev)
    view = View(WIDTH, HEIGHT, ev)
    apply_fn(
        lambda x: ev.register_listener(x),
        [keybd, view, game],
    )
    game.run()

main()
