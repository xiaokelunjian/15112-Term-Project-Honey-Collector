# Bee.py

import pygame
import random
import time
import math

class Bee(pygame.sprite.Sprite):

    width = 100
    height = 111
    speed = 20
    speedLevel = 5

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        (self.x, self.y) = (x, y)
        self.width = Bee.width
        self.height = Bee.height
        self.dir = direction
        self.alert_R = 100
        self.speed = Bee.speed
        self.phase = 1
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bee_entire_1.png'),
            (Bee.width, Bee.height)), self.dir)

    def enterAlert(self, x, y):
        # to check if the mouse has clicked inside the alert zone
        d = ((x - self.x - self.width/2)**2 + 
            (y - self.y - self.height/2)**2)**.5
        return d < self.alert_R

    def move(self):
        rad = (self.dir/180)*math.pi
        self.x += self.speed * math.cos(rad)
        self.y -= self.speed * math.sin(rad)

    def switchPhase(self):
        if(self.phase == 1):
            self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bee_entire_2.png'),
            (Bee.width, Bee.height)), self.dir)
            self.phase = 2
        else:
            self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/bee_entire_1.png'), 
            (Bee.width, Bee.height)), self.dir)
            self.phase = 1

    def onTimerFired(self):
        self.move()
        self.switchPhase()

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))