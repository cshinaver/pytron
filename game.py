#!/usr/bin/python
# game.py

import logging

import pygame
from twisted.internet.task import LoopingCall
from twisted.internet import reactor

from event_manager import (
    TickEvent,
    QuitGameEvent,
    BeginGameEvent,
    RegisterPlayerEvent,
    PlayerSetIDEvent,
)
from view import Bike, View


class Game:
    def __init__(self, ev, WIDTH, HEIGHT):
        self.event_manager = ev
        self.keep_running = True
        self.sprites = {}
        self.player_id = 8
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def init_game(self):
        self.player_bike = Bike(id=self.player_id)
        self.sprites[self.player_id] = self.player_bike
        self.clock = pygame.time.Clock()
        self.view = View(
            self.WIDTH,
            self.HEIGHT,
            self.event_manager,
            self.sprites,
        )
        self.event_manager.register_listener(self.view)
        self.event_manager.post(PlayerSetIDEvent(self.player_id))

    def run(self):
        self.init_game()
        lc = LoopingCall(lambda: self.event_manager.post(TickEvent()))
        interval = 1.0/60
        lc.start(interval)

    def notify(self, event):
        if isinstance(event, QuitGameEvent):
            print "Thanks for playing!"
            self.keep_running = False
            pygame.quit()
            reactor.stop()
        elif isinstance(event, TickEvent):
            for bike in self.sprites.values():
                print "player {n} (x, y): ({x}, {y})".format(
                    n=bike.id,
                    x=bike.rect.centerx,
                    y=bike.rect.centery,
                )
        elif isinstance(event, BeginGameEvent):
            self.run()
        elif isinstance(event, RegisterPlayerEvent):
            id = event.id
            x = event.x
            y = event.y
            b = Bike(id=id, x=x, y=y)
            logging.info('Registering player {id} at ({x},{y})'.format(
                id=id,
                x=x,
                y=y,
            ))
            self.sprites[id] = b
