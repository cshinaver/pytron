#!/usr/bin/python
# view.py
import pygame
import logging

from event_manager import (
    TickEvent,
    QuitGameEvent,
    MoveCharactorEvent,
)

colors = [
        (255, 0, 0), (0, 255, 0), (0, 0, 255),
        (255, 255, 0), (0, 255, 255), (255, 0, 255),
        (4, 57, 60), (108, 200, 40), (239, 150, 206),
        ]


class View:
    def __init__(self, WIDTH, HEIGHT, ev, sprites, board):
        pygame.init()
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.event_manager = ev
        self.sprites = sprites
        self.board = GameBoard(WIDTH, HEIGHT, sprites)
        self.black = 0, 0, 0
        self.game_over = False

        self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))

    def tick(self):
        if not self.game_over:
            self.render()
            pygame.display.flip()
            self.board.update()

    def render(self):
        self.window.fill(self.black)
        self.drawGameBoard()
        self.draw_lines()
        for s in self.sprites.values():
            self.window.blit(s.image, s.rect)

    def drawGameBoard(self):
        for i in range(self.board.rows):
            for j in range(self.board.cols):
                pygame.draw.rect(self.window,self.board.color,
                        (i*self.board.xshft + self.board.x, j*self.board.yshft + self.board.y, self.board.xshft, self.board.yshft), 1)

    def draw_lines(self):
        for i,row in enumerate(self.board.board):
            for j,item in enumerate(row):
                if item is not 0:
                    pygame.draw.line(self.window, 
                            colors[item],
                            (i+self.board.x, j+self.board.y), 
                            (i+self.board.x, j+self.board.y),
                            )

    def notify(self, event):
        if isinstance(event, MoveCharactorEvent):
            for s in self.sprites.values():
                s.update(event.direction)
        if isinstance(event, TickEvent):
            self.tick()
        elif isinstance(event, QuitGameEvent):
            self.game_over = True


class Bike(pygame.sprite.Sprite):
    def __init__(self, id=1, x=440, y=440, image_path="bike.png"):
        self.id = id
        print "hi, im a bike"
        self.image_path = image_path
        self.image = pygame.image.load(self.image_path)
        self.image.set_colorkey((255, 255, 255))
        self.orig_image = self.image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.direction = 'UP'

    def update(self, direction):
        if direction == "UP" or direction == "DOWN":
            self.image = pygame.transform.rotate(self.orig_image, 0)
        else:
            self.image = pygame.transform.rotate(self.orig_image, 90)


class GameBoard:
    def __init__(self, WIDTH, HEIGHT, sprites):
        print "hi, im a board"
        self.sprites = sprites
        self.color = (47, 79, 79)
        self.rows = 14
        self.cols = 14
        self.width = WIDTH - 20 * 2
        self.height = HEIGHT - 20 * 2
        self.xshft = self.width / self.rows
        self.yshft = self.height / self.cols
        self.x = (WIDTH - self.width) / 2
        self.y = (HEIGHT - self.height) / 2
        self.make_board()

    def make_board(self):
        self.board = [[0 for x in range(self.width)] 
                for x in range(self.height)]

    def update(self):
        for s in self.sprites.values():
            logging.debug('Updating gameboard for bike {id} at ({x},{y})'.format(
                id=s.id,
                x=s.rect.centerx,
                y=s.rect.centery,
            ))
            self.board[s.rect.centerx-self.x][s.rect.centery-self.y] = s.id
            

