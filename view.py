#!/usr/bin/python
# view.py
import pygame
from event_manager import TickEvent


class View:
    def __init__(self, WIDTH, HEIGHT):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick(self):
        pass

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.tick()

class Sprite(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

class Bike(Sprite):
    def __init__(self):
        print "hi, im a bike"
