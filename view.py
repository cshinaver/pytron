#!/usr/bin/python
# view.py
import pygame
from event_manager import TickEvent


class View:
    def __init__(self, WIDTH, HEIGHT, ev):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.event_manager = ev

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick(self):
        pass

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.tick()
