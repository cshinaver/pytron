#!/usr/bin/python
# controller.py
import pygame
from event_manager import (
    TickEvent,
    QuitGameEvent,
    MoveCharactorEvent,
)


class MovementController:
    def __init__(self, ev, sprites):
        self.event_manager = ev
        self.sprites = sprites
        self.player_direction = "DOWN"

    def notify(self, event):
        if isinstance(event, TickEvent):
            player = self.sprites[0]
            ds = 10
            if self.player_direction == "LEFT":
                player.rect.centerx -= ds
            elif self.player_direction == "RIGHT":
                player.rect.centerx += ds
            elif self.player_direction == "UP":
                player.rect.centery -= ds
            elif self.player_direction == "DOWN":
                player.rect.centery += ds
        elif isinstance(event, MoveCharactorEvent):
            self.player_direction = event.direction


class KeyboardController:
    def __init__(self, ev):
        self.event_manager = ev

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.event_manager.post(QuitGameEvent())
                elif event.key == pygame.K_LEFT:
                    self.event_manager.post(MoveCharactorEvent("LEFT"))
                elif event.key == pygame.K_RIGHT:
                    self.event_manager.post(MoveCharactorEvent("RIGHT"))
                elif event.key == pygame.K_UP:
                    self.event_manager.post(MoveCharactorEvent("UP"))
                elif event.key == pygame.K_DOWN:
                    self.event_manager.post(MoveCharactorEvent("DOWN"))

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.handle_input()
