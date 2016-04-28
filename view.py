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
        self.black = 0, 0, 0

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick(self):
        self.render()
        pygame.display.flip()

    def render(self):
        # self.window.fill(self.black)
        for s in self.sprites:
            self.window.blit(s.image, s.rect)

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.tick()


class Bike(pygame.sprite.Sprite):
    def __init__(self, id=1, image_path="bike.png"):
        self.id = id
        print "hi, im a bike"
        self.image = pygame.image.load(image_path)
        self.image_path = image_path
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
