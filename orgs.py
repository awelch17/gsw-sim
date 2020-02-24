import pygame
import random

from utils import *

from simvars import *
from dynvars import *

GRASS_COLOR = pygame.Color("green")
DEAD_COLOR = pygame.Color(102, 62, 29)
SHEEP_COLOR = pygame.Color("white")
WOLF_COLOR = pygame.Color("red")

class Grass():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.regrow_timer = 0
    
    def die(self):
        if(GRASS_DIES):
            self.alive = False
            self.regrow_timer = GRASS_REGROW_TIME
    
    def tick(self):
        if(not self.alive):
            if(self.regrow_timer > 0):
                self.regrow_timer -= 1
            else:
                self.alive = True
                self.regrow_timer = 0
    
    def draw(self, surface):
        if(self.alive):
            pygame.draw.rect(surface, GRASS_COLOR, pygame.Rect(self.x * SCALE, self.y * SCALE, SCALE, SCALE))
        else:
            pygame.draw.rect(surface, DEAD_COLOR, pygame.Rect(self.x * SCALE, self.y * SCALE, SCALE, SCALE))

class Sheep():
    def __init__(self, parent, x=None, y=None):
        self.parent = parent
        self.energy = SHEEP_INITIAL_ENERGY
        self.x = x
        self.y = y

        if(self.x == None):
            self.x = random.randint(0, WIDTH - 1)
        if(self.y == None):
            self.y = random.randint(0, HEIGHT - 1)

    def die(self):
        self.parent.sheep.remove(self)

    def tick(self):
        self.energy -= SHEEP_ENERGY_LOSS
        if(self.energy <= 0):
            self.die()
        
        if(self.energy > MAX_ENERGY):
            self.energy = MAX_ENERGY

        if(self.parent.grass[(self.x, self.y)].alive and self.energy < MAX_ENERGY - SHEEP_FOOD_GAIN):
            self.parent.grass[(self.x, self.y)].die()
            self.parent.grass[(self.x, self.y + 1)].die()
            self.parent.grass[(self.x, self.y - 1)].die()
            self.parent.grass[(self.x + 1, self.y)].die()
            self.parent.grass[(self.x + 1, self.y + 1)].die()
            self.parent.grass[(self.x + 1, self.y - 1)].die()
            self.parent.grass[(self.x - 1, self.y)].die()
            self.parent.grass[(self.x - 1, self.y + 1)].die()
            self.parent.grass[(self.x - 1, self.y - 1)].die()
            self.energy += SHEEP_FOOD_GAIN

        if(self.energy > REPRODUCTION_THRESHOLD and random.random() < SHEEP_REPRODUCTION):
            self.parent.sheep.append(Sheep(self.parent, x=self.x, y=self.y))
        
        closest_wolf_x = None
        closest_wolf_y = None
        dcache = None

        for wolf in self.parent.wolves:
            if(wolf.x > self.x - SHEEP_VISION and wolf.x < self.x + SHEEP_VISION
            and wolf.y > self.y - SHEEP_VISION and wolf.y < self.y + SHEEP_VISION):
                if(dcache != None):
                    if(distance(self.x, self.y, wolf.x, wolf.y) < dcache):
                        closest_wolf_x = wolf.x
                        closest_wolf_y = wolf.y
                        dcache = distance(self.x, self.y, wolf.x, wolf.y)
                else:
                    closest_wolf_x = wolf.x
                    closest_wolf_y = wolf.y
                    dcache = distance(self.x, self.y, wolf.x, wolf.y)
        
        if(closest_wolf_x != None):
            newpos = roundvec(expand(invert(normalize(self.x, self.y, closest_wolf_x, closest_wolf_y) ) , SHEEP_SPEED ) )
            self.x += newpos[0]
            self.y += newpos[1]

            if(self.x < 0):
                self.x = 0
            if(self.x > WIDTH - 1):
                self.x = WIDTH - 1
            if(self.y < 0):
                self.y = 0
            if(self.y > HEIGHT - 1):
                self.y = HEIGHT - 1
            
            return

        
        if(SHEEP_FLOCK):

            closest_sheep_x = None
            closest_sheep_y = None
            dcache = None
            for sheep in self.parent.sheep:
                if(sheep.x > self.x - SHEEP_VISION and sheep.x < self.x + SHEEP_VISION
                and sheep.y > self.y - SHEEP_VISION and sheep.y < self.y + SHEEP_VISION):
                    if(dcache != None):
                        if(distance(self.x, self.y, sheep.x, sheep.y) < dcache):
                            closest_sheep_x = sheep.x
                            closest_sheep_y = sheep.y
                            dcache = distance(self.x, self.y, sheep.x, sheep.y)
                    else:
                        closest_sheep_x = sheep.x
                        closest_sheep_y = sheep.y
                        dcache = distance(self.x, self.y, sheep.x, sheep.y)

            if(closest_sheep_x != None):
                newpos = roundvec(expand(normalize(self.x, self.y, closest_sheep_x, closest_sheep_y) , SHEEP_SPEED ) )
                self.x += newpos[0]
                self.y += newpos[1]
                if(self.x < 0):
                    self.x = 0
                if(self.x > WIDTH - 1):
                    self.x = WIDTH - 1
                if(self.y < 0):
                    self.y = 0
                if(self.y > HEIGHT - 1):
                    self.y = HEIGHT - 1

                return
        
        self.x += round((random.random() - 0.5) * 2 * SHEEP_SPEED)
        self.y += round((random.random() - 0.5) * 2 * SHEEP_SPEED)
        if(self.x < 0):
            self.x = 0
        if(self.x > WIDTH - 1):
            self.x = WIDTH - 1
        if(self.y < 0):
            self.y = 0
        if(self.y > HEIGHT - 1):
            self.y = HEIGHT - 1
    
    def draw(self, surface):
        pygame.draw.rect(surface, SHEEP_COLOR, pygame.Rect(self.x * SCALE, self.y * SCALE, SCALE, SCALE))

class Wolf():
    def __init__(self, parent, x=None, y=None):
        self.parent = parent
        self.energy = WOLF_INITIAL_ENERGY
        self.x = x
        self.y = y

        if(self.x == None):
            self.x = random.randint(0, WIDTH - 1)
        if(self.y == None):
            self.y = random.randint(0, HEIGHT - 1)

    def die(self):
        self.parent.wolves.remove(self)
    
    def tick(self):
        self.energy -= WOLF_ENERGY_LOSS
        if(self.energy <= 0):
            self.die()
        
        if(self.energy > MAX_ENERGY):
            self.energy = MAX_ENERGY
        
        if(self.energy < WOLF_FOOD_GAIN):
        
            for sheep in self.parent.sheep:
                if(distance(self.x, self.y, sheep.x, sheep.y) < WOLF_HUNTING_REACH):
                    if(random.random() < WOLF_HUNTING_SKILL):
                        sheep.die()
                        self.energy += WOLF_FOOD_GAIN
                        break
        
        if(self.energy > REPRODUCTION_THRESHOLD and random.random() < WOLF_REPRODUCTION):
            self.parent.wolves.append(Wolf(self.parent, x=self.x, y=self.y))
        
        closest_sheep_x = None
        closest_sheep_y = None
        dcache = None
        
        for sheep in self.parent.sheep:
            if(sheep.x > self.x - WOLF_VISION and sheep.x < self.x + WOLF_VISION
            and sheep.y > self.y - WOLF_VISION and sheep.y < self.y + WOLF_VISION):
                if(dcache != None):
                    if(distance(self.x, self.y, sheep.x, sheep.y) < dcache):
                        closest_sheep_x = sheep.x
                        closest_sheep_y = sheep.y
                        dcache = distance(self.x, self.y, sheep.x, sheep.y)
                else:
                    closest_sheep_x = sheep.x
                    closest_sheep_y = sheep.y
                    dcache = distance(self.x, self.y, sheep.x, sheep.y)
        
        if(closest_sheep_x != None):
            newpos = roundvec(expand(normalize(self.x, self.y, closest_sheep_x, closest_sheep_y), WOLF_SPEED ) )
            self.x += newpos[0]
            self.y += newpos[1]

            if(self.x < 0):
                self.x = 0
            if(self.x > WIDTH - 1):
                self.x = WIDTH - 1
            if(self.y < 0):
                self.y = 0
            if(self.y > HEIGHT - 1):
                self.y = HEIGHT - 1
            
            return

        self.x += round((random.random() - 0.5) * 2 * WOLF_SPEED)
        self.y += round((random.random() - 0.5) * 2 * WOLF_SPEED)
        if(self.x < 0):
            self.x = 0
        if(self.x > WIDTH - 1):
            self.x = WIDTH - 1
        if(self.y < 0):
            self.y = 0
        if(self.y > HEIGHT - 1):
            self.y = HEIGHT - 1


    def draw(self, surface):
        pygame.draw.rect(surface, WOLF_COLOR, pygame.Rect(self.x * SCALE, self.y * SCALE, SCALE * 2, SCALE * 2))