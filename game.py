#!/usr/bin/python
# game.py

import pygame
from event_manager import TickEvent, QuitGameEvent


class Game:
    def __init__(self, ev):
        self.event_manager = ev
        self.keep_running = True

    def run(self):
        while self.keep_running:
            self.event_manager.post(TickEvent())

    def notify(self, event):
        if isinstance(event, QuitGameEvent):
            print "Thanks for playing!"
            self.keep_running = False
            pygame.quit()
