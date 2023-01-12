import pygame
from pygame.locals import *
import numpy as np


switch = lambda value: not(value)

def check_event(mouse):
    for event in pygame.event.get():
        if event.type == QUIT:
            return "quit"
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                return "quit"
            if event.key == K_SPACE:
                return "pause"
        if event.type in (pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
            mouse(event.type, event.pos)


def check_collision_planet(a, b):
            r = a.r + b.r
            return r <= np.linalg.norm(a.cords - b.cords)
