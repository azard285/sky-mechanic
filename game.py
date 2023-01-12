import pygame
import numpy as np 

import config as cg
from menu import Button
from func import check_event, switch
from objects import Point, Points


class Game:
    def __init__(self):
        self.init_game()

        self.width, self.height = cg.Screen_size
        self.screen = pygame.display.set_mode(cg.Screen_size, pygame.DOUBLEBUF)
        self.clock = pygame.time.Clock()

        self.pause = False
        self.FPS = 60

        self.points = Points([
            Point((683, 383), mass=2 * 10 ** 20,  color=pygame.Color("yellow"), speed=np.array([0, 0])),
            Point((983, 383), mass=0.2, r=10, speed=np.array([0, 10]), show_path=True)]) # Попробуй заменить show_path на show_particle и посмотри что изменилось
        self.particles = []

        self.pause_menu = Button(self.width // 2, self.height // 2, 2, 2, "Play", padding=6, on_click=self.pause_switch)

    def init_game(self):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption("sky mechanic")

    def run(self):
        while True:
            event = check_event(self.pause_menu.handle_mouse_event)
            if event == "quit":
                self.exit()
            elif event == "pause":
                self.pause_switch()

            self.screen.fill((0, 15, 32))

            if self.pause:  
                if self.particles:
                    for particle in self.particles:
                        particle.draw(self.screen)

                self.points.draw(self.screen)
                self.pause_menu.draw(self.screen)  
            else:
                self.points.create_particle(self.particles)
                if self.particles:
                    for particle in self.particles:
                        if particle.age >= particle.max_age:
                            self.particles.remove(particle)
                        particle.draw(self.screen)
                        particle.move()

                self.points.draw(self.screen)
                self.points.move(.5)

            pygame.display.update()
            self.clock.tick(self.FPS)

    def pause_switch(self):
        self.pause = switch(self.pause)

    @staticmethod
    def exit():
        pygame.quit()
        exit()


if __name__ == '__main__':
    game = Game()
    game.run()
