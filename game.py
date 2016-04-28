#!/usr/bin/python
# game.py

import pygame
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from event_manager import TickEvent, QuitGameEvent
from view import Bike


class Game:
    def __init__(self, ev):
        self.event_manager = ev
        self.keep_running = True
        self.sprites = []
        self.player_id = 8

    def init_game(self):
        self.player_bike = Bike(id=self.player_id)
        self.sprites.append(self.player_bike)
        self.clock = pygame.time.Clock()

    def run(self):
        self.init_game()
        lc = LoopingCall(lambda: self.event_manager.post(TickEvent()))
        interval = 1.0/60
        lc.start(interval)
        reactor.run()

    def notify(self, event):
        if isinstance(event, QuitGameEvent):
            print "Thanks for playing!"
            self.keep_running = False
            pygame.quit()
            reactor.stop()
        elif isinstance(event, TickEvent):
            print "player (x, y): ({x}, {y})".format(
                x=self.player_bike.rect.centerx,
                y=self.player_bike.rect.centery,
            )
