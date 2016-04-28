#!/usr/bin/python
# view.py
import pygame
from event_manager import TickEvent


class View:
    def __init__(self, WIDTH, HEIGHT, ev, sprites):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.event_manager = ev
        self.sprites = sprites

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
    def __init__(self, image_path="bike.png"):
        print "hi, im a bike"
        self.image = image_path
        self.rect = self.image.get_rect()
        self.rect.centerx = 200
        self.rect.centery = 200
