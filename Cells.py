# Cells.py

import pygame
import random
import time
import math
from Color import Color

class Cell(object):

    size = 50
    edge = 3
    width = size * 3**.5
    height = size * 3

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.size = Cell.size
        self.width = Cell.width
        self.height = Cell.height
        self.isunraveled = False
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_1.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)
        self.flip = False

    def draw(self, screen):
        screen.blit(self.image, (self.x, self.y))

    def isMouseClicked(self, x, y):
        if(x > self.x and x < self.x + Cell.width
            and x + 3**.5*y > self.x + 3**.5*(self.y+self.size/2) 
            and x + 3**.5*y < self.x + 3**.5*(self.y+5*self.size/2)
            and x - 3**.5*y > self.x - 3**.5*(self.y+3*self.size/2)
            and x - 3**.5*y < self.x - 3**.5*(self.y-self.size/2)):
            return True
        else:
            return False

    def switch(self):
        self.flip = True
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_2.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)

    def onTimerFired(self):
        pass

class CellWithHoney(Cell):

    amount = 10

    def __init__(self, x, y):
        super().__init__(x, y)
        self.amount = 5
        self.type = "honey"
        self.empty = False
        self.scoreFont = pygame.font.SysFont(None, 25)
        self.scoreRising = 5
        self.scorePace = 0

    def switch(self):
        if(not self.flip):
            self.flip = True
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_honey.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
        elif(self.flip and not self.empty):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_2.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.empty = True

    def draw(self, screen):
        super().draw(screen)
        if(self.empty and self.scorePace < 10):
            screen_text = self.scoreFont.render(
                "+%d" % CellWithHoney.amount, True, Color.darkGreen)
            score_text_X = self.x + self.width/2 - 10 
            # Hard coding here! Will be removed.
            score_text_Y = self.y + self.height/2 - 10 - self.scoreRising * self.scorePace 
            # Hard coding here! Will be removed.
            screen.blit(screen_text, (score_text_X, score_text_Y))

    def onTimerFired(self):
        if(self.empty):
            self.scorePace += 1

class CellWithLarva(Cell):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "larva"
        self.phase = 0
        self.irritated = False
        self.exploded = False
        self.breeded = False
        self.countDown = 30
        self.countDownText = pygame.font.SysFont(None, 25)

    def switch(self):
        if(not self.flip):
            self.flip = True
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_larva_1.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = 1
        elif(self.flip and self.countDown >= 0 and not self.irritated):
            self.irritated = True

    def draw(self, screen):
        super().draw(screen)
        if(self.flip and self.countDown >= 0):
            screen_text = self.countDownText.render("%d" % self.countDown, 
                True, Color.red)
            countDown_X = self.x + self.width/2 - 5
            countDown_Y = self.y + self.height/4 - 20
            screen.blit(screen_text, (countDown_X, countDown_Y))

    def switchPhase(self):
        if(self.countDown < 0):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_2.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = -1
        elif(self.countDown > 10 and self.phase == 1):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_larva_2.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = 2
        elif(self.countDown > 10 and self.phase == 2):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_larva_1.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = 1
        elif(self.countDown <= 10 and self.phase == 1):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_larva_4.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = 2
        elif(self.countDown <= 10 and self.phase == 2):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_larva_3.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
            self.phase = 1

    def explode(self):
        self.countDown = -1
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_2.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)
        self.phase = -1
        self.exploded = True

    def onTimerFired(self):
        self.switchPhase()
        if(self.flip):
            self.countDown -= 1

class CellWithPupa(Cell):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "pupa"
        self.health = 10
        self.countDown = 30
        self.killed = False
        self.breeded = False
        self.flip = True
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_pupa.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)
        self.countDownText = pygame.font.SysFont(None, 25)
        self.healthText = pygame.font.SysFont(None, 25)

    def switch(self):
        pass

    def damage(self):
        self.health -= 1

    def kill(self):
        self.killed = True
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_2.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)

    def breed(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_2.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)
        self.breeded = True

    def onTimerFired(self):
        self.countDown -= 1

    def draw(self, screen):
        super().draw(screen)
        if(self.countDown >= 0 and not self.killed):
            countDown_text = self.countDownText.render("%d" % self.countDown,
                True, Color.red)
            countDown_X = self.x + self.width/2 - 5
            countDown_Y = self.y + self.height/4 - 20
            screen.blit(countDown_text, (countDown_X, countDown_Y))
            health_Text = self.healthText.render("%d" % self.health, True, 
                Color.green)
            health_X = self.x + self.width/2 - 5
            health_Y = self.y + self.height/4 + 20
            screen.blit(health_Text, (health_X, health_Y))

class CellWithBee(Cell):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "bee"

    def switch(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_bee.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)

class CellWithGuard(Cell):

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "guard"

    def switch(self):
        self.image = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/cell_guard.png').convert_alpha(),
            (round(3**.5*self.size), 2*self.size)), 0)

class CellWithQueen(Cell):

    bonus = 100

    def __init__(self, x, y):
        super().__init__(x, y)
        self.type = "queen"
        self.wink = 0
        self.queenText = pygame.font.SysFont(None, 25)
        self.rising = 5
        self.countDown = 150
        self.collected = False
        self.countDownText = pygame.font.SysFont(None, 25)

    def switch(self):
        if(not self.flip):
            self.flip = True
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_queen_1.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)

    def switchPhase(self):
        if(self.flip and self.wink and self.wink % 2 == 1):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_queen_2.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)
        elif(self.flip):
            self.image = pygame.transform.rotate(pygame.transform.scale(
                pygame.image.load('images/cell_queen_1.png').convert_alpha(),
                (round(3**.5*self.size), 2*self.size)), 0)

    def draw(self, screen):
        super().draw(screen)
        if(self.flip and self.wink < 20):
            screen_text = self.queenText.render(
                "+%d" % CellWithQueen.bonus, True, Color.purple)
            queen_text_X = self.x + self.width/2 - 35
            queen_text_Y = self.y + self.height/2 - self.wink * self.rising
            screen.blit(screen_text, (queen_text_X, queen_text_Y))
        if(self.flip and self.countDown >= 0):
            countDown_text = self.countDownText.render(
                "%d" % self.countDown, True, Color.red)
            countDown_X = self.x + self.width/2 - 5
            countDown_Y = self.y + self.height/4 - 20
            screen.blit(countDown_text, (countDown_X, countDown_Y))

    def onTimerFired(self):
        self.switchPhase()
        if(self.flip):
            self.wink += 1
            self.countDown -= 1