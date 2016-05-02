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
    PlayerDeath,
    RemotePlayerDeath,
)
from view import Bike, GameBoard, View


class Game:
    def __init__(self, ev, WIDTH, HEIGHT):
        self.event_manager = ev
        self.keep_running = True
        self.sprites = {}
        self.board = GameBoard(WIDTH, HEIGHT, self.sprites)
        self.player_id = 8
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

    def init_game(self):
        self.clock = pygame.time.Clock()
        self.view = View(
            self.WIDTH,
            self.HEIGHT,
            self.event_manager,
            self.sprites,
            self.board
        )
        self.event_manager.register_listener(self.view)

    def run(self):
        self.init_game()
        lc = LoopingCall(lambda: self.event_manager.post(TickEvent()))
        interval = 1./120
        lc.start(interval)

    def notify(self, event):
        if isinstance(event, QuitGameEvent):
            print "Thanks for playing!"
            self.keep_running = False
            pygame.quit()
            reactor.stop()
        elif isinstance(event, TickEvent):
            pass
            #for bike in self.sprites.values():
            #    print "player {n} (x, y): ({x}, {y})".format(
            #        n=bike.id,
            #        x=bike.rect.centerx,
            #        y=bike.rect.centery,
            #    )
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
        elif isinstance(event, PlayerDeath):
            logging.info('Player ' + str(event.id) + ' died')
            del self.sprites[event.id]
        elif isinstance(event, RemotePlayerDeath):
            logging.info('Player ' + str(event.id) + ' died')
            del self.sprites[event.id]
