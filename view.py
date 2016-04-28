#!/usr/bin/python
# view.py
import pygame


class View:
    def __init__(self, WIDTH, HEIGHT):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick():
        pass

    def notify(self, event):
        pass
