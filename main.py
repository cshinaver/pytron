#!/usr/bin/python
# main.py
import pygame

from view import View


WIDTH = 340
HEIGHT = 480


def main():
    View(WIDTH, HEIGHT)
    while 1:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    print "l"

main()
