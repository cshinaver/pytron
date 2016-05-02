#!/usr/bin/python
# controller.py

import logging

import pygame
from event_manager import (
    TickEvent,
    QuitGameEvent,
    LocalMoveCharactorEvent,
    RemoteMoveCharactorEvent,
    PlayerSetIDEvent,
)


class MovementController:
    def __init__(self, ev, sprites, board):
        self.event_manager = ev
        self.sprites = sprites
        self.board = board
        self.player_direction = "DOWN"

    def notify(self, event):
        if isinstance(event, TickEvent):
            for bike in self.sprites.values():
                ds = 1
                if bike.direction == "LEFT":
                    bike.rect.centerx -= ds
                elif bike.direction == "RIGHT":
                    bike.rect.centerx += ds
                elif bike.direction == "UP":
                    bike.rect.centery -= ds
                elif bike.direction == "DOWN":
                    bike.rect.centery += ds
                self.dectectcollision(bike)
        elif isinstance(event, LocalMoveCharactorEvent):
            logging.info('Setting {id} direction to {d}'.format(
                id=event.id,
                d=event.direction,
            ))
            self.sprites[event.id].direction = event.direction
        elif isinstance(event, RemoteMoveCharactorEvent):
            logging.info('Setting {id} direction to {d}'.format(
                id=event.id,
                d=event.direction,
            ))
            self.sprites[event.id].direction = event.direction
        elif isinstance(event, PlayerSetIDEvent):
            self.player_id = event.id

    def dectectcollision(self, bike):
        if (bike.direction == "LEFT" and bike.rect.centerx < 30) or self.board.get_adjusted_position(bike.rect.centerx, bike.rect.centery) != 0:
            del(bike)
            print "collision"
        elif (bike.direction == "RIGHT" and bike.rect.centerx > 445) or self.board.get_adjusted_position(bike.rect.centerx, bike.rect.centery) != 0:
            del(bike)
            print "collision"
        elif (bike.direction == "UP" and bike.rect.centery < 30) or self.board.get_adjusted_position(bike.rect.centerx, bike.rect.centery) != 0:
            del(bike)
            print "collision"
        elif (bike.direction == "DOWN" and bike.rect.centery > 445) or self.board.get_adjusted_position(bike.rect.centerx, bike.rect.centery) != 0:
            del(bike)
            print "collision"


class KeyboardController:
    def __init__(self, ev):
        self.event_manager = ev

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.event_manager.post(QuitGameEvent())
                elif event.key == pygame.K_LEFT:
                    self.event_manager.post(
                        LocalMoveCharactorEvent(self.player_id, "LEFT"),
                    )
                elif event.key == pygame.K_RIGHT:
                    self.event_manager.post(
                        LocalMoveCharactorEvent(self.player_id, "RIGHT"),
                    )
                elif event.key == pygame.K_UP:
                    self.event_manager.post(
                        LocalMoveCharactorEvent(self.player_id, "UP"),
                    )
                elif event.key == pygame.K_DOWN:
                    self.event_manager.post(
                        LocalMoveCharactorEvent(self.player_id, "DOWN"),
                    )

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.handle_input()
        elif isinstance(event, PlayerSetIDEvent):
            self.player_id = event.id
