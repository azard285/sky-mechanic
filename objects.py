from math import cos, sin
from os import path
from random import randint, randrange

import pygame
import pygame.gfxdraw
import numpy as np

import config as cg
from func import check_collision_planet


class Points:
    def __init__(self, points):
        self.points = points

    def clean_acc(self):
        for point in self.points:
            point.clean_acc()

    def move(self, dt):
        self.clean_acc()
        self.get_force()
        for point in self.points:
            point.accelerate(dt)
            point.move(dt)

    def get_force(self):
        for a in self.points:
            for b in self.points:
                if a == b:
                    continue

                pa, pb = a.cords, b.cords
                ma, mb = a.mass, b.mass
                delta = np.linalg.norm(pa-pb)
                if delta < 0.001:
                    continue
                if not check_collision_planet(a, b):
                    a.speed *= -0.8
                    a.speed[0][0] = a.speed[0][0]*cos(180) + a.speed[0][1]*sin(180)
                    a.speed[0][1] = a.speed[0][1]*cos(180) - a.speed[0][0]*sin(180)
                    continue
                force = cg.G * (ma * mb) / ((delta * 10000) ** 2)
                a.accinc(force, pb)

    def draw(self, screen):
        for point in self.points:
            point.draw(screen)

    def create_particle(self, particles):
        for point in self.points:
            if not point.show_particle:
                continue
            i = randrange(10)
            if i < 4:
                for _ in range(i):
                    particle = Particle((point.cords[0][0] + randint(-1, 1), point.cords[0][1] + randint(-1, 1)), max_age=randint(10, 100))
                    particles.append(particle)


    def __iter__(self, *args, **kwargs):
        return (point for point in self.points)

class Point:
    def __init__(self, cords, r=25, mass=1.0, color=(200, 0, 0), speed=None, show_particle=False,  show_path=False, **properties):
        self.r = r
        self.color = color
        self.cords = np.array([cords], float)
        if speed is None:
            self.speed = np.array([0 for i in range(len(cords))], float)
        else:
            self.speed = speed
        self.acc = np.array([0 for i in range(len(cords))], float)
        self.mass = mass
        self.__params__ = ["cords", "speed", "acc"] + list(properties.keys())

        self.show_particle = show_particle
        self.show_path = show_path
        self.path = []
        for property in properties:
            setattr(self, property, properties[property])

    def move(self, dt):

        self.path.append(self.cords)
        if len(self.path) > 500:
            self.path.pop(0)

        self.cords = self.cords + self.speed * dt

    def accelerate(self, dt):
        self.speed = self.speed + self.acc * dt

    def accinc(self, force, pb):
        self.acc = (self.acc + (pb - self.cords) * (force/self.mass))

    def clean_acc(self):
        self.acc = self.acc * 0

    def draw(self, screen):
        if self.show_path:
            if len(self.path) > 5:
                for i in self.path:
                    pygame.gfxdraw.pixel(screen, int(i[0][0]), int(i[0][1]),[255, 255, 255])
        pygame.draw.circle(screen, self.color, self.cords[0], self.r)

    def __str__(self):
        r = ["Point {"]
        for p in self.__params__:
            r.append(" " + p + " = " + str(getattr(self, p)))
        r += ["}"]
        return "\n".join(r)

class Particle:
    def __init__(self, cords, r=1, color=(150, 150, 0, .5), max_age=100):
        self.color = color
        self.cords = list(cords)
        self.r = r
        self.max_age = max_age
        self.age = 0

    def move(self):
        self.age += randint(0, 2)
        self.cords[0] += randint(-1, 1)
        self.cords[1] += randint(-1, 1)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.cords, self.r)

class TextObject:
    def __init__(self, x, y, text_func, color, font_name, font_size):
        self.pos = (x, y)
        self.text_func = text_func
        self.color = color
        self.font = pygame.font.SysFont(font_name, font_size)
        self.text_surface, self.bounds = self.get_surface(text_func())
    
    def draw(self, screen):
        text_surface, self.bounds = self.get_surface(self.text_func())

        pos = (self.pos[0] - self.bounds.width // 2, self.pos[1])
        screen.blit(text_surface, pos)
    
    def get_surface(self, text):
        text_surface = self.font.render(text, False, self.color)

        return text_surface, text_surface.get_rect()
    
    def update(self):
        pass
