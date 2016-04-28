#!/usr/bin/python
# controller.py
import pygame
from event_manager import TickEvent


class KeyboardController:
    def __init__(self, ev):
        self.event_manager = ev

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_l:
                    print "l"

    def notify(self, event):
        if isinstance(event, TickEvent):
            self.handle_input()
