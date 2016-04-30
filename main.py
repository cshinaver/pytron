#!/usr/bin/python
# main.py

from controller import KeyboardController
from controller import MovementController
from event_manager import EventManager
from game import Game
from utils import apply_fn
from network import begin_on_client_connect
from twisted.internet import reactor


WIDTH = 480
HEIGHT = 480


def main():
    ev = EventManager()
    game = Game(ev, WIDTH, HEIGHT)
    keybd = KeyboardController(ev)
    movement_controller = MovementController(ev, game.sprites)
    apply_fn(
        lambda x: ev.register_listener(x),
        [
            keybd,
            game,
            movement_controller,
        ],
    )
    begin_on_client_connect(ev)
    reactor.run()

main()
