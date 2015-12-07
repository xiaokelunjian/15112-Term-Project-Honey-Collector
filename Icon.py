# Icon.py

import pygame
import random
import math
import time
from Color import Color

class Icon(object):

    def __init__(self, x, y, color, size):
        (self.x, self.y) = (x, y)
        self.color = color
        self.size = size
        self.width = int(self.size*3**.5)
        self.height = 2*self.size

    def isMouseOn(self, x, y):
        if(x > self.x - (self.size*3**.5)/2 
            and x < self.x + (self.size*3**.5)/2
            and x + 3**.5*y > self.x + 3**.5*(self.y-self.size) 
            and x + 3**.5*y < self.x + 3**.5*(self.y+self.size)
            and x - 3**.5*y > self.x - 3**.5*(self.y+self.size)
            and x - 3**.5*y < self.x - 3**.5*(self.y-self.size)):
            return True
        else:
            return False

    def draw(self, screen):
        pygame.draw.polygon(screen, self.color, [(self.x, self.y - self.size), 
            (self.x + (self.size*3**.5)/2, self.y - self.size/2),
            (self.x + (self.size*3**.5)/2, self.y + self.size/2),
            (self.x, self.y + self.size),
            (self.x - (self.size*3**.5)/2, self.y + self.size/2),
            (self.x - (self.size*3**.5)/2, self.y - self.size/2)], 0)

class IntroIcon(Icon):
    
    def __init__(self, x, y, color, title, size = 100):
        super().__init__(x, y, color, size)
        self.title = title
        self.fontColor = Color.black
        self.font = pygame.font.SysFont("Comic Sans MS", 25)
        self.iconText = self.font.render(self.title, True, self.fontColor)
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("images/cell_2.png"), 
            (int(3**.5*self.size), 2*self.size)), 0)

    def mouseOn(self):
        self.fontColor = Color.red
        self.iconText = self.font.render(self.title, True, self.fontColor)
        self.size = 150
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("images/cell_2.png"), 
            (int(3**.5*self.size), 2*self.size)), 0)

    def mouseOff(self):
        self.fontColor = Color.black
        self.iconText = self.font.render(self.title, True, self.fontColor)
        self.size = 100
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load("images/cell_2.png"), 
            (int(3**.5*self.size), 2*self.size)), 0)

    def mouseClick(self):
        self.fontColor = Color.darkGreen
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def draw(self, screen):
        screen.blit(self.image, 
            (self.x - (3**.5*self.size)//2, self.y - (2*self.size)//2))
        screen.blit(self.iconText, 
            (self.x - 100, self.y - 20))

class InstroIcon(Icon):

    def __init__(self, x, y, color, title, size = 50):
        super().__init__(x, y, color, size)
        self.title = title
        self.fontColor = Color.black
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def mouseOn(self):
        self.fontColor = Color.red
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.size = 100
        # self.draw(screen)

    def mouseOff(self):
        self.fontColor = Color.black
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.size = 50
        # self.draw(screen)

    def mouseClick(self):
        self.fontColor = Color.darkGreen
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.draw(screen)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.iconText, (self.x - self.width/2, self.y - 10))

class GameIcon(Icon):

    width = int(50*3**.5)

    def __init__(self, x, y, color, title, size = 50):
        super().__init__(x, y, color, size)
        self.title = title
        self.fontColor = Color.black
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def mouseOn(self):
        self.fontColor = Color.red
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.size = 100

    def mouseOff(self):
        self.fontColor = Color.black
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def mouseClick(self):
        self.fontColor = Color.darkGreen
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.iconText, (self.x - self.width/2, self.y - 10))

class BoxIcon(Icon):

    width = int(50*3**.5)

    def __init__(self, x, y, color, title, size = 50):
        super().__init__(x, y, color, size)
        self.title = title
        self.fontColor = Color.black
        self.font = pygame.font.SysFont("Comic Sans MS", 15)
        self.iconText = self.font.render(self.title, True, self.fontColor)

    def mouseOn(self):
        self.fontColor = Color.red
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.size = 100
        # self.draw(screen)

    def mouseOff(self):
        self.fontColor = Color.black
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.size = 50
        # self.draw(screen)

    def mouseClick(self):
        self.fontColor = Color.darkGreen
        self.iconText = self.font.render(self.title, True, self.fontColor)
        # self.draw(screen)

    def draw(self, screen):
        super().draw(screen)
        screen.blit(self.iconText, (self.x - self.width/2, self.y - 10))
