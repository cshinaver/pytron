#!/usr/bin/python
# main.py

from view import View
from event_manager import EventManager, TickEvent
from controller import KeyboardController
from utils import apply_fn


WIDTH = 480
HEIGHT = 480


def main():
    ev = EventManager()
    keybd = KeyboardController()
    view = View(WIDTH, HEIGHT)
    apply_fn(
        lambda x: ev.register_listener(x),
        [keybd, view],
    )

    while 1:
        ev.post(TickEvent())

main()
