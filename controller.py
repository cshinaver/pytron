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
        self.player_direction = "LEFT"

    def notify(self, event):
        if isinstance(event, TickEvent):
            for bike in self.sprites:
                ds = 1
                if bike.direction == "LEFT":
                    bike.rect.centerx -= ds
                elif bike.direction == "RIGHT":
                    bike.rect.centerx += ds
                elif bike.direction == "UP":
                    bike.rect.centery -= ds
                elif bike.direction == "DOWN":
                    bike.rect.centery += ds
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
