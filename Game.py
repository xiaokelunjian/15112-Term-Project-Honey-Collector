# Game.py
# citing from: https://github.com/LBPeraza/Pygame-Asteroids

import pygame
import random
import math
import time
from Cells import *
from Bee import Bee
from Color import Color
from Icon import *

class Game(object):

    def __init__(self, startX, startY, width = 1000, height = 800, FPS = 24):
        self.width = width
        self.height = height
        self.start_X = startX
        self.start_Y = startY
        self.initPygame()
        self.buffer = 10
        self.title = "Honey Collector"
        self.FPS = FPS
        self.font = pygame.font.SysFont("Comic Sans MS", 45)
        self.subFont = pygame.font.SysFont("Comic Sans MS", 25)
        self.scoreInit()
        self.cellInit()
        self.beeInit()
        self.iconsInit()
        self.gameControllerInit()
        self.larvaCount = 0
        self.boxSize = 200
        self.level = None
        self.winBonus = 300

    def initPygame(self):
        pygame.init()
        self.gameDisplay = pygame.display.set_mode((self.width, self.height))

    def scoreInit(self):
        self.jarWidth = self.height//10
        self.jarHeight = self.height//10
        self.jar_X = self.buffer
        self.jar_Y = self.height - self.jarHeight - self.buffer
        self.jarImage = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/honey_jar.png').convert_alpha(),
            (self.jarWidth, self.jarHeight)), 0)
        self.score = 0
        self.score_X = self.jar_X + self.jarWidth + 2*self.buffer
        self.score_Y = self.height - self.jarHeight/2 - self.buffer
        self.scoreFont = pygame.font.SysFont("Comic Sans MS", 25)

    def addCell(self, index, x, y, maxIndex):
        if(index == 1):
            self.cellList.append(CellWithQueen(x, y))
        elif(index < maxIndex//4):
            self.cellList.append(CellWithLarva(x, y))
        else:
            self.cellList.append(CellWithHoney(x, y))

    def cellInit(self):
        self.cellList = [ ]
        rows = int((self.height - 2 * self.start_Y)//Cell.height)
        cols = int((self.width - 2 * self.start_X)//Cell.width)
        maxIndex = 2*rows*cols+1
        indexList = list(range(1, maxIndex))
        random.shuffle(indexList)
        for row in range(rows):
            for col in range(cols):
                # for one line:
                cell_type_index = indexList.pop(0)
                cell_X = self.start_X + col * (Cell.width - Cell.edge)
                cell_Y = self.start_Y + row * (Cell.height - 2 * Cell.edge)
                self.addCell(cell_type_index, cell_X, cell_Y, maxIndex)
                # for the other line:
                cell_type_index = indexList.pop(0)
                cell_X = self.start_X + (col + 0.5) * (Cell.width - Cell.edge)
                cell_Y = self.start_Y + (row + 0.5) * (Cell.height - 2 * Cell.edge)
                self.addCell(cell_type_index, cell_X, cell_Y, maxIndex)

    def beeInit(self):
        self.beeCount = 3
        self.beeList = pygame.sprite.Group()
        for i in range(self.beeCount):
            beeX = random.randint(self.buffer, 
                self.width - Bee.width - self.buffer)
            beeY = random.randint(self.buffer,
                self.height - Bee.height - self.buffer)
            direction = random.randint(0, 359)
            self.beeList.add(Bee(beeX, beeY, direction))

    def iconsInit(self):
        # initialize box icons:
        self.restartIcon = BoxIcon(2*self.width//5, 7*self.height//10, 
            Color.orange, "  RESTART")
        self.quitIcon = BoxIcon(3*self.width//5, 7*self.height//10,
            Color.pink, "      QUIT")
        self.resumeIcon = BoxIcon(2*self.width//5, 7*self.height//10, 
            Color.lime, "   RESUME")
        # initialize game icons:
        self.gameIconDist = GameIcon.width
        self.pauseIcon = GameIcon(self.width - 2*self.gameIconDist, 
            self.jar_Y + 2*self.buffer, Color.cyan, "     PAUSE")

    def gameControllerInit(self):
        self.gameExit = False
        self.gameStart = False
        self.gamePaused = False
        self.gameStop = False

    def scoreDisplay(self, x, y, color):
        scoreText = self.scoreFont.render("HONEY: %d" % self.score, 
            True, color)
        self.gameDisplay.blit(scoreText, [x, y])

    def run(self):
        pygame.display.set_caption(self.title)
        clock = pygame.time.Clock()
        # game surface display:
        while(not self.gameExit):
            self.runGame()
            clock.tick(self.FPS)
        return
        # pygame.quit()
        # quit()

    def runIntroduction(self):
        # run the instruction surface
        self.gameDisplay.blit(self.introFace, (0, 0))
        self.playIcon.draw(self.gameDisplay)
        self.introQuitIcon.draw(self.gameDisplay)
        self.instructionIcon.draw(self.gameDisplay)
        pygame.display.update()
        for event in pygame.event.get():
            self.playIconRelated(event)
            self.introQuitIconRelated(event)
            self.instructionIconRelated(event)

    def isGameStart(self):
        for cell in self.cellList:
            if(cell.flip):
                return True
        return False

    def gameEvent(self):
        # runs when the game has not really started or has come to an end:
        for event in pygame.event.get():
            if(event.type == pygame.QUIT):
                self.gameExit = True
            elif(self.isGameStart()):
                self.gameStart = True
            self.mousePressed(event)
            self.mouseMoved(event)

    def mouseMoved(self, event):
        self.pauseIconRelated(event)

    def mousePressed(self, event):
        if(event.type == pygame.MOUSEBUTTONDOWN):
            for cell in self.cellList:
                if(cell.isMouseClicked(*pygame.mouse.get_pos())):
                    cell.switch()
                    if(cell.type == "honey" and cell.empty):
                        self.score += CellWithHoney.amount
                    elif(cell.type == "queen" and cell.flip 
                        and not cell.collected):
                        self.score += CellWithQueen.bonus
                        cell.collected = True
                    elif(cell.type == "pupa" and not cell.killed):
                        cell.damage()
                        if(cell.health <= 0):
                            cell.kill()
                    elif(cell.type == "larva" and cell.flip
                        and cell.countDown <= 10):
                        cell.explode()
                    pygame.display.update()
            if(self.pauseIcon.isMouseOn(*pygame.mouse.get_pos())):
                self.gamePaused = True
        # print(self.gamePaused)

    def drawScoreRelated(self):
        self.gameDisplay.blit(self.jarImage, (self.jar_X, self.jar_Y))
        self.scoreDisplay(self.score_X, self.score_Y, Color.black)

    def drawGameIcon(self):
        self.pauseIcon.draw(self.gameDisplay)

    def scoreTimerFired(self):
        if(self.score > 0):
            self.score -= 1

    def modifyBorder(self, bee):
        if(bee.x + bee.width < 0):
            bee.x = self.width
        elif(bee.x > self.width):
            bee.x = - bee.width
        if(bee.y + bee.height < 0):
            bee.y = self.height
        elif(bee.y > self.height):
            bee.y = - bee.height

    def modifyDirection(self, bee):
        (event_x, event_y) = pygame.mouse.get_pos()
        delta_X = event_x - (bee.x + bee.width/2)
        delta_Y = event_y - (bee.y + bee.height/2)
        if(delta_X == 0):
            if(delta_Y > 0):
                event_angle = 270
            elif(delta_Y < 0):
                event_angle = 90
        elif(delta_X > 0):
            event_angle = (math.atan(- delta_Y/delta_X)/2*math.pi)*360
        elif(delta_X < 0):
            event_angle = (math.atan(-delta_Y/delta_X)/2*math.pi)*360 + 180
        if(event_angle > (bee.dir % 360)):
            bee.dir += 10
        elif(event_angle < (bee.dir % 360)):
            bee.dir -= 10
        bee.speed = Bee.speed

    def beesTimerFired(self):
        for bee in self.beeList:
            bee.speed += Bee.speedLevel * self.larvaCount
            bee.draw(self.gameDisplay)
            bee.onTimerFired()
            self.modifyBorder(bee)
            self.modifyDirection(bee)

    def cellTimerFired(self):
        self.larvaCount = 0
        for cell in self.cellList:
            cell.draw(self.gameDisplay)
            cell.onTimerFired()
            if(cell.type == "larva" and cell.flip and cell.countDown >= 0):
                self.larvaCount += 1  
            if(cell.type == "larva" and cell.flip and cell.countDown <= -3
                and not cell.exploded and not cell.breeded):
                # direction = random.randint(0, 359)
                # self.beeList.add(Bee(cell.x, 
                #     cell.y, direction))
                # self.beeCount += 1
                new_x, new_y = cell.x, cell.y
                self.cellList.remove(cell)
                self.cellList.append(CellWithPupa(new_x, new_y))
            if(cell.type == "pupa" and cell.countDown <= -3 and not cell.killed
                and not cell.breeded):
                direction = random.randint(0, 359)
                self.beeList.add(Bee(cell.x, 
                    cell.y, direction))
                self.beeCount += 1
                cell.breed()
                pygame.display.update()
            if(cell.type == "queen" and cell.countDown <= -3):
                direction = random.randint(0, 359)
                self.beeList.add(Bee(cell.x, 
                    cell.y, direction))
                self.beeCount += 1

    def gameMessage(self, msg, color, x, y):
        screenText = self.font.render(msg, True, color)
        self.gameDisplay.blit(screenText, [x, y])

    def gameSubMessage(self, color, x, y):
        screenSubText = self.subFont.render("   HONEY COLLECTED: %d" % self.score, 
            True, color)
        self.gameDisplay.blit(screenSubText, [x, y])

    def drawJumpBox(self, msg, color1, fontColor, color2, x, y, size):
        pygame.draw.polygon(self.gameDisplay, color1, [(x, y - size), 
            (x + (size*3**.5)/2, y - size/2),(x + (size*3**.5)/2, y + size/2),
            (x, y + size),(x - (size*3**.5)/2, y + size/2),
            (x - (size*3**.5)/2, y - size/2)], 0)
        self.gameMessage(msg, fontColor, x - (size*3**.5)/2, y - size/2)
        self.gameSubMessage(fontColor, x - (size*3**.5)/2, y)

    def displayGameOver(self):
        # self.gameMessage("GAME OVER",Color.red,
        #     self.width/2 - 15*self.buffer, self.height/2 - self.buffer)
        # self.gameMessage("Press 'r' to restart or 'q' to exit", Color.red,
        #     self.width/2 - 25*self.buffer, self.height/2 + self.buffer)
        self.drawJumpBox("   GAME OVER", Color.blonde, Color.red, Color.orange, 
            self.width/2, self.height/2, self.boxSize)
        self.restartIcon.draw(self.gameDisplay)
        self.quitIcon.draw(self.gameDisplay)
        pygame.display.update()
        # time.sleep(2)
        # self.gameExit = True

    def isGameOver(self):
        for cell in self.cellList:
            if(cell.type == "larva" and cell.countDown > 10 and cell.irritated):
                self.gameStop = True
                self.displayGameOver()
        for bee in self.beeList:
            if(self.gameStart and bee.enterAlert(*pygame.mouse.get_pos())):
                self.gameStop = True
                self.displayGameOver()

    def displayGameWin(self):
        # self.gameMessage("YOU WIN", Color.green,
        #     self.width/2 - 8*self.buffer, self.height/2 - self.buffer)
        # self.gameMessage("HONEY: %d" % self.score, Color.green
        #     self.width/2 - 8*self.buffer, self.height/2 + self.buffer)
        self.drawJumpBox("    YOU WIN!!", Color.blonde, Color.green, Color.orange, 
            self.width/2, self.height/2, self.boxSize)
        bonusFont = pygame.font.SysFont("Comic Sans MS", 20)
        bonusText = bonusFont.render("                   +BONUS:%d" % self.winBonus, 
            True, Color.green)
        self.gameDisplay.blit(bonusText, (self.width//2 - (self.boxSize*3**.5)//2,
            self.height//2 - self.boxSize//4))
        self.restartIcon.draw(self.gameDisplay)
        self.quitIcon.draw(self.gameDisplay)
        pygame.display.update()
        # time.sleep(2)
        # self.gameExit = True

    def isGameWin(self):
        for cell in self.cellList:
            if(cell.flip == False):
                return
        self.gameStop = True
        self.score += self.winBonus
        self.displayGameWin()

    def displayGamePause(self):
        self.drawJumpBox("  GAME PAUSE", Color.violet, Color.grey, Color.orange, 
            self.width/2, self.height/2, self.boxSize)
        self.resumeIcon.draw(self.gameDisplay)
        self.quitIcon.draw(self.gameDisplay)
        pygame.display.update()

    def isGamePause(self):
        return self.gamePaused

    def pauseIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.pauseIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.pauseIcon.mouseOn()
            pygame.display.update()
        # elif(event.type == pygame.MOUSEBUTTONDOWN and
        #     self.pauseIcon.isMouseOn(*pygame.mouse.get_pos())):
        #     self.pauseIcon.mouseClick()
        #     pygame.display.update()
        #     self.gamePaused = False
        else:
            self.pauseIcon.mouseOff()

    def restartIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.restartIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.restartIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.restartIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.restartIcon.mouseClick()
            pygame.display.update()
            self.restartGame()
        else:
            self.restartIcon.mouseOff()
            # pygame.display.update()
        # print(self.restartIcon.size)
        # pygame.display.update()

    def quitIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.quitIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.quitIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.quitIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.quitIcon.mouseClick()
            pygame.display.update()
            self.gameExit = True
        else:
            self.quitIcon.mouseOff()

    def resumeIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.resumeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.resumeIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.resumeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.resumeIcon.mouseClick()
            pygame.display.update()
            self.gamePaused = False
        else:
            self.resumeIcon.mouseOff()

    def runGame(self):
        if(not self.gameStop and not self.gamePaused):
            # run the game surface
            self.gameEvent()
            self.gameDisplay.fill(Color.cream)
            self.drawScoreRelated()
            self.drawGameIcon()
            # cell related part:
            self.cellTimerFired()
            # bee related part:
            self.beesTimerFired()
            # score related part:
            self.scoreTimerFired()
            # check win or lose:
            self.isGameOver()
            self.isGameWin()
            pygame.display.update()
        elif(not self.gameStop and self.gamePaused):
            self.displayGamePause()
            for event in pygame.event.get():
                self.resumeIconRelated(event)
                self.quitIconRelated(event)
            pygame.display.update()
        else:
            for event in pygame.event.get():
                self.restartIconRelated(event)
                self.quitIconRelated(event)
            self.restartIcon.draw(self.gameDisplay)
            self.quitIcon.draw(self.gameDisplay)
            pygame.display.update()

    def restartGame(self):
        self.__init__(self.start_X, self.start_Y)