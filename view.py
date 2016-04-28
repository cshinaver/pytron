#!/usr/bin/python
# view.py
import pygame
from event_manager import (
    TickEvent,
    QuitGameEvent,
    MoveCharactorEvent,
)


class View:
    def __init__(self, WIDTH, HEIGHT, ev, sprites):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.event_manager = ev
        self.sprites = sprites
        self.board = GameBoard()
        self.black = 0, 0, 0

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick(self):
        self.render()
        pygame.display.flip()

    def render(self):
        self.window.fill(self.black)
        self.drawGameBoard()
        for s in self.sprites:
            self.window.blit(s.image, s.rect)

    def drawGameBoard(self):
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                pygame.draw.rect(self.window,self.board.color,
                        (i*self.board.xshft + self.board.x, j*self.board.yshft + self.board.y, self.board.xshft, self.board.yshft), 1)

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.tick()
        if isinstance(event, MoveCharactorEvent):
            self.sprites[0].update(event.direction)


class Bike(pygame.sprite.Sprite):
    def __init__(self, id=1, image_path="bike.png"):
        self.id = id
        print "hi, im a bike"
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.image.set_colorkey((255, 255, 255))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0

    def update(self, direction):
        print "updating direction to: ",direction
        if direction == "UP" or direction == "DOWN":
            print "in up or down", direction
            self.image = pygame.transform.rotate(self.orig_image, 0)
        else:
            print "in left or right", direction
            self.image = pygame.transform.rotate(self.orig_image, 90)
            



class GameBoard:
    def __init__(self):
        print "hi, im a board"
        self.color = (47, 79, 79)
        self.width = 440
        self.height = 440
        self.rows = 14
        self.cols = 14
        self.xshft = self.width / self.rows
        self.yshft = self.height / self.cols
        self.x = (480 - self.width) / 2
        self.y = (480 - self.height) / 2
