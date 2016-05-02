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
    RemoteMovePlayer,
    LocalMovePlayer,
    PlayerCollision,
    PlayerDeath,
)


class MovementController:
    def __init__(self, ev, sprites, board):
        self.event_manager = ev
        self.sprites = sprites
        self.board = board
        self.player_direction = "DOWN"
        self.tick_index = 1
        self.move_player = True

    def notify(self, event):
        if isinstance(event, TickEvent):
            if not self.move_player:
                return
            if not self.tick_index % 3:
                bike = self.sprites[self.player_id]
                ds = 3
                if bike.direction == "LEFT":
                    bike.rect.centerx -= ds
                elif bike.direction == "RIGHT":
                    bike.rect.centerx += ds
                elif bike.direction == "UP":
                    bike.rect.centery -= ds
                elif bike.direction == "DOWN":
                    bike.rect.centery += ds
                self.dectectcollision(bike)
                self.tick_index = 1
            else:
                self.tick_index += 1
            if self.move_player:
                e = LocalMovePlayer(
                    self.player_id,
                    self.sprites[self.player_id].rect.centerx,
                    self.sprites[self.player_id].rect.centery,
                )
                self.event_manager.post(e)
        elif isinstance(event, RemoteMovePlayer):
            self.sprites[event.id].rect.centerx = event.x
            self.sprites[event.id].rect.centery = event.y
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
        elif isinstance(event, PlayerCollision):
            logging.info("Player " + str(event.player_id) + " died.")
            self.event_manager.post(PlayerDeath(event.player_id))
        elif isinstance(event, PlayerDeath):
            self.move_player = False

    def dectectcollision(self, bike):
        cid = self.board.get_adjusted_position(bike.rect.centerx, bike.rect.centery)
        if cid:
            logging.debug("collision {pid1} with {pid2}".format(
                pid1=bike.id,
                pid2=cid,
                ))
            e = PlayerCollision(player_id=bike.id, object_id=cid)
            self.event_manager.post(e)
        elif (bike.direction == "LEFT" and bike.rect.centerx < 30):
            logging.debug("collision {pid1} with {pid2}".format(
                pid1=bike.id,
                pid2=cid,
                ))
            self.event_manager.post(e)
        elif (bike.direction == "RIGHT" and bike.rect.centerx > 445):
            logging.debug("collision {pid1} with {pid2}".format(
                pid1=bike.id,
                pid2=cid,
                ))
            self.event_manager.post(e)
        elif (bike.direction == "UP" and bike.rect.centery < 30):
            logging.debug("collision {pid1} with {pid2}".format(
                pid1=bike.id,
                pid2=cid,
                ))
            self.event_manager.post(e)
        elif (bike.direction == "DOWN" and bike.rect.centery > 445):
            logging.debug("collision {pid1} with {pid2}".format(
                pid1=bike.id,
                pid2=cid,
                ))
            self.event_manager.post(e)


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
