import pygame

from simvars import *
from dynvars import INITIAL_SHEEP_COUNT, INITIAL_WOLF_COUNT
import orgs

class Map():
    def __init__(self):
        self.grass = {}
        self.sheep = []
        self.wolves = []

        for x in range(-1, WIDTH + 1):
            for y in range(-1, HEIGHT + 1):
                self.grass[(x, y)] = orgs.Grass(x, y)

        for i in range(0, INITIAL_SHEEP_COUNT):
            self.sheep.append(orgs.Sheep(self))
        
        for i in range(0, INITIAL_WOLF_COUNT):
            self.wolves.append(orgs.Wolf(self))

    def display_stats(self):
        grass_counter = 0

        for grass in self.grass.values():
            if(grass.alive):
                grass_counter += 1
            
        pygame.display.set_caption("GSW-SIM: " + str(grass_counter) + " grass, " + str(len(self.sheep)) + " sheep, " + str(len(self.wolves)) + " wolves")

    def tick(self):
        for grass in self.grass.values():
            grass.tick()
        
        for sheep in self.sheep:
            sheep.tick()
        
        for wolf in self.wolves:
            wolf.tick()
    
    def draw(self, surface):
        for grass in self.grass.values():
            grass.draw(surface)
        
        for sheep in self.sheep:
            sheep.draw(surface)
        
        for wolf in self.wolves:
            wolf.draw(surface)