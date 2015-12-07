#Main.py

import pygame
from pygame.locals import *
import random
import math
import time
from Color import Color
from Icon import *
from Game import Game

class GameFrame(object):

    def __init__(self, width = 1000, height = 800, FPS = 24):
        pygame.init()
        self.playing = True
        self.selectionMode = False
        self.width = width
        self.height = height
        self.bannerHeight = height - 60
        self.startX = None
        self.startY = None
        self.level = None
        self.frameDisplay = pygame.display.set_mode((self.width, self.height))
        self.FPS = FPS
        self.title = "Honey Collector"
        self.introInit()
        self.iconsInit()
        self.instructionInit()
        self.highScoreInit()

    def introInit(self):
        self.enterIntro = True
        self.introFace = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/intro.gif').convert_alpha(),
            (self.width, self.height)), 0)

    def iconsInit(self):
        self.playIcon = IntroIcon(2*self.width//5, 3*self.height//5, 
            Color.white, "          PLAY")
        self.quitIcon = IntroIcon(3*self.width//5, 4*self.height//5,
            Color.white, "          EXIT")
        self.instructionIcon = IntroIcon(3*self.width//5, 2*self.height//5, 
            Color.white,"     TUTORIAL")
        self.highScoreIcon = IntroIcon(4*self.width//5, 3*self.height//5,
            Color.white,"   HIGH SCORE")
        # initialize mode selection icons:
        self.easyModeIcon = InstroIcon(2*self.width//5, 2*self.height//5,
            Color.cyan,"      EASY")
        self.mediumModeIcon = InstroIcon(2*self.width//5, 3*self.height//5,
            Color.lime, "   MEDIUM")
        self.hardModeIcon = InstroIcon(2*self.width//5, 4*self.height//5,
            Color.pink, "      HARD")
        # initialize instruction icons:
        self.backIcon = InstroIcon(self.width//4, self.bannerHeight,
            Color.lime, "      BACK")
        self.forwardIcon = InstroIcon(3*self.width//4, self.bannerHeight,
            Color.cyan, " FORWARD")
        self.mainMenuIcon = InstroIcon(self.width//2, self.bannerHeight,
            Color.violet, "      MENU")
        # initialize high score icons:
        self.mainMenuIconII = InstroIcon(self.width//10, self.bannerHeight, 
            Color.violet, "      MENU")
        self.resetIcon = InstroIcon(9*self.width//10, self.bannerHeight,
            Color.pink, "     RESET")
        self.yesIcon = BoxIcon(2*self.width//5, 7*self.height//10, 
            Color.cyan, "       YES")
        self.noIcon = BoxIcon(3*self.width//5, 7*self.height//10, 
            Color.pink, "        NO")
        self.OKIcon = BoxIcon(self.width//2, 4*self.height//5,
            Color.pink, "        OK")

    def instructionInit(self):
        self.instroIndex = 0
        self.enterInstro = False
        instroFace_1 = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/instruction_1.gif').convert_alpha(),
            (self.width, self.height)), 0)
        instroFace_2 = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/instruction_2.gif').convert_alpha(),
            (self.width, self.height)), 0)
        instroFace_3 = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/instruction_3.gif').convert_alpha(),
            (self.width, self.height)), 0)
        instroFace_4 = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/instruction_4.gif').convert_alpha(),
            (self.width, self.height)), 0)
        self.instructionFace = [instroFace_1, instroFace_2, 
            instroFace_3, instroFace_4]

    def highScoreInit(self):
        self.enterHighScore = False
        self.jumpScreen = False
        self.getName = False
        self.highScoreFace = pygame.transform.rotate(pygame.transform.scale(
            pygame.image.load('images/high_score.gif').convert_alpha(),
            (self.width, self.height)), 0)

    def run(self):
        pygame.display.set_caption(self.title)
        while(self.playing):
            self.frameDisplay.blit(self.introFace, (0, 0))
            self.playIcon.draw(self.frameDisplay)
            self.quitIcon.draw(self.frameDisplay)
            self.instructionIcon.draw(self.frameDisplay)
            self.highScoreIcon.draw(self.frameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                self.playIconRelated(event)
                self.quitIconRelated(event)
                self.instructionIconRelated(event)
                self.highScoreIconRelated(event)
                pygame.display.update()
        self.quitFrame()

    def playIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.playIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.playIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.playIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.playIcon.mouseClick()
            self.selectionMode = True
            self.runLevelSelection()
        else:
            self.playIcon.mouseOff()

    def quitIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.quitIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.quitIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.quitIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.quitIcon.mouseClick()
            self.playing = False
        else:
            self.quitIcon.mouseOff()

    def instructionIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.instructionIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.instructionIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.instructionIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.instructionIcon.mouseClick()
            self.enterInstro = True
            self.runInstruction()
        else:
            self.instructionIcon.mouseOff()

    def highScoreIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.highScoreIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.highScoreIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.highScoreIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.highScoreIcon.mouseClick()
            self.enterHighScore = True
            self.runHighScore()
        else:
            self.highScoreIcon.mouseOff()

    def easyModeIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.easyModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.easyModeIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.easyModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.easyModeIcon.mouseClick()
            self.startX = 200
            self.startY = 200
            self.level = "easy"
            self.runGame()
        else:
            self.easyModeIcon.mouseOff()

    def mediumModeIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.mediumModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.mediumModeIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.mediumModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.mediumModeIcon.mouseClick()
            self.startX = 130
            self.startY = 130
            self.level = "medium"
            self.runGame()
        else:
            self.mediumModeIcon.mouseOff()

    def hardModeIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.hardModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.hardModeIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.hardModeIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.hardModeIcon.mouseClick()
            self.startX = 50
            self.startY = 50
            self.level = "hard"
            self.runGame()
        else:
            self.hardModeIcon.mouseOff()

    def OKIconRelated(self, event, name):
        if(event.type == pygame.MOUSEMOTION and
            self.OKIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.OKIcon.mouseOn()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.OKIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.OKIcon.mouseClick()
            self.getName = False
            return name
        else:
            self.OKIcon.mouseOff()

    def runLevelSelection(self):
        while(self.selectionMode):
            self.easyModeIcon.draw(self.frameDisplay)
            self.mediumModeIcon.draw(self.frameDisplay)
            self.hardModeIcon.draw(self.frameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                self.easyModeIconRelated(event)
                self.mediumModeIconRelated(event)
                self.hardModeIconRelated(event)
                pygame.display.update()
                if(event.type == pygame.MOUSEBUTTONDOWN and 
                    not self.easyModeIcon.isMouseOn(*pygame.mouse.get_pos()) and 
                    not self.mediumModeIcon.isMouseOn(*pygame.mouse.get_pos()) and
                    not self.hardModeIcon.isMouseOn(*pygame.mouse.get_pos())):
                    self.selectionMode = False

    def runGame(self):
        game = Game(self.startX, self.startY)
        game.run()
        print("self.level:", self.level)
        self.setScoreList(game.score, self.level)
        self.run()

    def writeFile(self, path, contents):
        # citing from: http://www.cs.cmu.edu/~112/notes/notes-strings.html
        with open(path, "wt") as f:
            f.write(contents)

    def readLevelRecords(self, level):
        if(level == "hard"):
            return self.readFile("records/scorelist_H.txt")
        elif(level == "medium"):
            return self.readFile("records/scorelist_M.txt")
        elif(level == "easy"):
            return self.readFile("records/scorelist_E.txt")

    def setScoreList(self, curScore, level):
        currScoreText = self.readLevelRecords(level)
        print(currScoreText)
        nameScoreList = [ ]
        index = 0
        while(index < 3):
            line = currScoreText.splitlines()[index]
            score = int(line.split("/")[0])
            name = line.split("/")[1]
            nameScoreList.append((score, name))
            index += 1
        # newName = input("Please enter your name:")
        if(curScore > nameScoreList[-1][0]):
            self.getName = True
            newName = self.getNewName()
            curIndex = self.findIndex(curScore, nameScoreList)
            largerPart = nameScoreList[:curIndex]
            smallerPart = nameScoreList[curIndex:]
            newScoreList = largerPart + [(curScore, newName)] + smallerPart
            newScoreList.pop()
            self.writeScoreList(newScoreList, level)
        else:
            return

    def getNewName(self):
        name = "No name"
        while(self.getName):
            self.drawJumpBoxII()
            self.OKIcon.draw(self.frameDisplay)
            nameFont = pygame.font.SysFont("Comic Sans MS", 15)
            for event in pygame.event.get():
                # mouse event related:
                if(event.type == pygame.MOUSEMOTION and
                    self.OKIcon.isMouseOn(*pygame.mouse.get_pos())):
                    self.OKIcon.mouseOn()
                elif(event.type == pygame.MOUSEBUTTONDOWN and
                    self.OKIcon.isMouseOn(*pygame.mouse.get_pos())):
                    self.OKIcon.mouseClick()
                    self.getName = False
                    return name
                else:
                    self.OKIcon.mouseOff()
                # key event related:
                # citing from: https://gist.github.com/ohsqueezy/4428513
                if(event.type == KEYDOWN):
                    if(event.unicode.isalpha()):
                        name += event.unicode
                    elif(event.key == K_BACKSPACE):
                        name = name[:-1]
                    elif(event.key == K_SPACE):
                        name += " "
            block = nameFont.render(name, True, Color.black)
            rect = block.get_rect()
            rect.center = (self.width//2, self.height//2 + 100)
            self.frameDisplay.blit(block, rect)
            pygame.display.flip()

    def drawJumpBoxII(self):
        size = 200
        x = self.width//2
        y = self.height//2
        pygame.draw.polygon(self.frameDisplay, Color.cyan, [(x, y - size), 
            (x + (size*3**.5)/2, y - size/2),(x + (size*3**.5)/2, y + size/2),
            (x, y + size),(x - (size*3**.5)/2, y + size/2),
            (x - (size*3**.5)/2, y - size/2)], 0)
        boxFont = pygame.font.SysFont("Comic Sans MS", 30)
        boxSubFont = pygame.font.SysFont("Comic Sans MS", 15)
        congText = boxFont.render("  CONGRATULATIONS!!", True, Color.red)
        msgText = boxSubFont.render("                         You've on the records!", 
            True, Color.red)
        plzText = boxSubFont.render("  Please enter your name(less than 30 letters):", 
            True, Color.red)
        self.frameDisplay.blit(congText, (x - (size*3**.5)//2, y - size//2))
        self.frameDisplay.blit(msgText, (x - (size*3**.5)//2, y - size//4))
        self.frameDisplay.blit(plzText, (x - (size*3**.5)//2, y))

    def findIndex(self, score, nameList):
        for i in range(len(nameList)):
            if(score > nameList[i][0]):
                return i

    def writeScoreList(self, newList, level):
        newContent = ""
        for pair in newList:
            newContent += str(pair[0]) + "/" + pair[1] + "\n"
        if(level == "hard"):
            self.writeFile("records/scorelist_H.txt", newContent) 
        elif(level == "medium"):
            self.writeFile("records/scorelist_M.txt", newContent)
        elif(level == "easy"):
            self.writeFile("records/scorelist_E.txt", newContent)

    def backIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.backIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.backIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.backIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.backIcon.mouseClick()
            pygame.display.update()
            self.instroIndex -= 1
        else:
            self.backIcon.mouseOff()

    def forwardIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.forwardIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.forwardIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.forwardIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.forwardIcon.mouseClick()
            pygame.display.update()
            self.instroIndex += 1
        else:
            self.forwardIcon.mouseOff()

    def mainMenuIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.mainMenuIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.mainMenuIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.mainMenuIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.mainMenuIcon.mouseClick()
            pygame.display.update()
            self.enterInstro = False
        else:
            self.mainMenuIcon.mouseOff()

    def runInstruction(self):
        while(self.enterInstro):
            self.frameDisplay.blit(self.instructionFace[self.instroIndex], (0, 0))
            self.mainMenuIcon.draw(self.frameDisplay)
            if(self.instroIndex > 0):
                self.backIcon.draw(self.frameDisplay)
            if(self.instroIndex < len(self.instructionFace) -1):
                self.forwardIcon.draw(self.frameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                self.backIconRelated(event)
                self.forwardIconRelated(event)
                self.mainMenuIconRelated(event)
                if(not self.enterInstro):
                    self.run()
                    return

    def mainMenuIconIIRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.mainMenuIconII.isMouseOn(*pygame.mouse.get_pos())):
            self.mainMenuIconII.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.mainMenuIconII.isMouseOn(*pygame.mouse.get_pos())):
            self.mainMenuIconII.mouseClick()
            pygame.display.update()
            self.enterHighScore = False
        else:
            self.mainMenuIconII.mouseOff()

    def resetIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.resetIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.resetIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.resetIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.resetIcon.mouseClick()
            pygame.display.update()
            self.jumpScreen = True
            self.resetConfirmation()
        else:
            self.resetIcon.mouseOff()

    def drawJumpBox(self):
        size = 200
        x = self.width//2
        y = self.height//2
        pygame.draw.polygon(self.frameDisplay, Color.yellow, [(x, y - size), 
            (x + (size*3**.5)/2, y - size/2),(x + (size*3**.5)/2, y + size/2),
            (x, y + size),(x - (size*3**.5)/2, y + size/2),
            (x - (size*3**.5)/2, y - size/2)], 0)
        boxFont = pygame.font.SysFont("Comic Sans MS", 30)
        textLine1 = boxFont.render("        Are you sure", True, Color.black)
        textLine2 = boxFont.render("   to reset high score?", True, Color.black)
        self.frameDisplay.blit(textLine1, (x - (size * 3**.5)//2, y - size//2))
        self.frameDisplay.blit(textLine2, (x - (size * 3**.5)//2, y - size//4))

    def yesIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.yesIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.yesIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.yesIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.yesIcon.mouseClick()
            pygame.display.update()
            self.resetHighScore()
            self.jumpScreen = False
        else:
            self.yesIcon.mouseOff()

    def noIconRelated(self, event):
        if(event.type == pygame.MOUSEMOTION and
            self.noIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.noIcon.mouseOn()
            pygame.display.update()
        elif(event.type == pygame.MOUSEBUTTONDOWN and
            self.noIcon.isMouseOn(*pygame.mouse.get_pos())):
            self.noIcon.mouseClick()
            pygame.display.update()
            self.jumpScreen = False
        else:
            self.noIcon.mouseOff()

    def resetConfirmation(self):
        while(self.jumpScreen):
            self.drawJumpBox()
            self.yesIcon.draw(self.frameDisplay)
            self.noIcon.draw(self.frameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                self.yesIconRelated(event)
                self.noIconRelated(event)

    def resetHighScore(self):
        resetText = self.readFile("records/initial.txt")
        self.writeFile("records/scorelist_H.txt", resetText)
        self.writeFile("records/scorelist_M.txt", resetText)
        self.writeFile("records/scorelist_E.txt", resetText)

    def readFile(self, path):
        # citing from: http://www.cs.cmu.edu/~112/notes/notes-strings.html
        with open(path, "rt")as f:
            return f.read()

    def loadScore(self, text, startPos):
        listFont = pygame.font.SysFont("Comic Sans MS", 30)
        lineDist = 50
        index = 0
        while(index < 3):
            line = text.splitlines()[index]
            color = Color.red if index == 0 else Color.black
            rankText = listFont.render(str(index + 1), True, color)
            scoreText = listFont.render(line.split("/")[0], True, color)
            nameText = listFont.render(line.split("/")[1], True, color)
            textY = startPos + (index+1) * lineDist
            self.frameDisplay.blit(rankText, (3*self.width//10, textY))
            self.frameDisplay.blit(scoreText, (5*self.width//10, textY))
            self.frameDisplay.blit(nameText, (7*self.width//10, textY))
            index += 1

    def placeScoreTitle(self):
        titleFont = pygame.font.SysFont("Comic Sans MS", 40)
        rankTitle = titleFont.render("RANK", True, Color.black)
        scoreTitle = titleFont.render("SCORE", True, Color.black)
        nameTitle = titleFont.render("NAME", True, Color.black)
        easyTitle = titleFont.render("EASY", True, Color.black)
        mediumTitle = titleFont.render("MEDIUM", True, Color.black)
        hardTitle = titleFont.render("HARD", True, Color.black)
        startPos = self.height//8 + 100
        block = 190
        self.frameDisplay.blit(hardTitle , (self.width//10, 
            startPos))
        self.frameDisplay.blit(mediumTitle, (self.width//10,
            startPos + block))
        self.frameDisplay.blit(easyTitle, (self.width//10,
            startPos + 2*block))
        self.frameDisplay.blit(rankTitle , (3*self.width//10, self.height//8))
        self.frameDisplay.blit(scoreTitle, (5*self.width//10, self.height//8))
        self.frameDisplay.blit(nameTitle, (7*self.width//10, self.height//8))

    def runHighScore(self):
        while(self.enterHighScore):
            self.frameDisplay.blit(self.highScoreFace, (0, 0))
            hardScoreText = self.readFile("records/scorelist_H.txt")
            mediumScoreText = self.readFile("records/scorelist_M.txt")
            easyScoreText = self.readFile("records/scorelist_E.txt")
            self.placeScoreTitle()
            block = 190
            startPos = self.height//8
            self.loadScore(hardScoreText, startPos)
            startPos += block
            self.loadScore(mediumScoreText, startPos)
            startPos += block
            self.loadScore(easyScoreText, startPos)
            self.mainMenuIconII.draw(self.frameDisplay)
            self.resetIcon.draw(self.frameDisplay)
            pygame.display.update()
            for event in pygame.event.get():
                self.mainMenuIconIIRelated(event)
                self.resetIconRelated(event)
                if(not self.enterHighScore):
                    self.run()
                    return

    def quitFrame(self):
        pygame.quit()
        quit()

def main():
    frame = GameFrame()
    frame.run()

if(__name__ == '__main__'):
    main()