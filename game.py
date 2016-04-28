#!/usr/bin/python
# game.py

import pygame
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
        while self.keep_running:
            self.clock.tick(60)
            self.event_manager.post(TickEvent())
            print "player (x, y): ({x}, {y})".format(
                x=self.player_bike.rect.centerx,
                y=self.player_bike.rect.centery,
            )

    def notify(self, event):
        if isinstance(event, QuitGameEvent):
            print "Thanks for playing!"
            self.keep_running = False
            pygame.quit()
