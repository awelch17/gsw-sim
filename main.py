from sys import exit
import pygame
import sim

from simvars import *

pygame.init()

pygame.display.set_caption("GSW-SIM")
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))

if(__name__ == "__main__"):
    simmap = sim.Map()

    while(True):
        screen.fill(pygame.Color("white"))
        simmap.tick()
        simmap.display_stats()
        simmap.draw(screen)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
