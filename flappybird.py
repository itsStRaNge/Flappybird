#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import shelve
import operator
#import serial

useSensors = False
numberOfPlayers = 1
screenWidth = 1200
screenHeight = 640
numberOfWalls = 3
wallSpawn = 1000
distanceOfBirds = 126
music = "music/main.mp3"
#clickerIDs = ["01a7fd15","01a7fe21","01a7c30b"]
#keys = [K_UP,K_DOWN,K_RIGHT,K_LEFT]
#names = ["nico","clemens","luis","jakob"]
pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

class Players:
    clickerIDs = ["01a7fd15", "01a7fe21", "01a7c30b"]
    keys = [K_UP, K_DOWN, K_RIGHT, K_LEFT]
    names = ["nico", "clemens", "luis", "jakob"]
    colors = [(0,0,255),(0,255,0),(255,0,0),(120,0,120)]

class Wall:
    def __init__(self, id, flappybird):
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 150
        self.offset = random.randint(-(screenHeight*0.2), screenHeight*0.4)
        self.id = id
        self.wallx = screenWidth+ self.id*300
        self.upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        self.movementType = 1
        self.directionOfMovement = 1
        self.wallspeed = 6
        self.flappybird = flappybird

    def offsetMovement(self):
        # self.offset = random.randint(-110, 110)
        if self.directionOfMovement == 1 and self.offset < screenHeight*0.4:
            self.offset += 1

            if self.offset >= -(screenHeight*0.2):
                self.directionOfMovement = 2

        elif self.directionOfMovement == 2:
            self.offset -= 1

            if self.offset <=  -(screenHeight*0.2):
                self.directionOfMovement = 1

    def updateGap(self):
        if self.directionOfMovement == 2 and self.gap < 200:
            self.gap += 4

            if self.gap >= 200:
                self.directionOfMovement = 1

        elif self.directionOfMovement == 1:
            self.gap -= 4

            if self.gap <= 150:
                self.directionOfMovement = 2

    def updateWallPosition(self):
        self.wallx -= self.wallspeed

        if self.wallx < -80:
            self.wallx = screenWidth
            self.offset = random.randint(-(screenHeight*0.2), screenHeight*0.4)
            self.movementType = random.randint(1, 3)
            self.wallspeed += 0.2
            self.flappybird.counter += 1
            for i in range(0,numberOfPlayers):
                if not self.flappybird.bird[i].dead:
                    self.flappybird.bird[i].counter += 1

        if self.movementType == 2:
            self.updateGap()
        elif self.movementType == 3:
            self.offsetMovement()
        self.upRect = pygame.Rect(self.wallx,
                                  360 + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                                    0 - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())

    def resetWalls(self):
        self.gap = 150
        self.offset = random.randint(-(screenHeight*0.2), screenHeight*0.4)
        self.wallx = screenWidth+ self.id*300
        self.upRect = pygame.Rect(self.wallx,
                                  360 + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                                    0 - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())
        self.movementType = 1
        self.directionOfMovement = 1
        self.wallspeed = 6
        self.flappybird.counter = 0

class Controller:
    def __init__(self):
        if(useSensors == True):
            self.ser = serial.Serial(
                port='/dev/ttyAMA0',
                baudrate = 9600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0
            )
    def updateSensor(self,flappyBird):
        numberOfBytesInInputBuffer = self.ser.inWaiting()
        if numberOfBytesInInputBuffer >= 14:
            receivedBytes = self.ser.read(14)
            clickerID = receivedBytes[8:12]
            clickerState = receivedBytes[4]

            if clickerState.encode('hex') == '10':
                for birdID in range(0,numberOfPlayers):
                    if flappyBird.bird[birdID].clickerID == clickerID.encode('hex') and not flappyBird.bird[birdID].dead:
                        flappyBird.bird[birdID].jump = 17
                        flappyBird.bird[birdID].gravity = 5
                        flappyBird.bird[birdID].jumpSpeed = 10
                        return 0
                    elif flappyBird.bird[birdID].clickerID == clickerID.encode('hex') and flappyBird.bird[birdID].dead:
                        return 1
        return 0
    def updateKeyboard(self,flappyBird):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN):  # and not self.bird[birdID].dead
                birdID = -1
                if (event.key == Players.keys[0]):
                    birdID = 0
                elif (event.key == Players.keys[1]):
                    birdID = 1
                elif (event.key == Players.keys[2]):
                    birdID = 2
                elif (event.key == Players.keys[3]):
                    birdID = 3
                if (birdID != -1 and birdID < numberOfPlayers and not flappyBird.bird[birdID].dead):
                    flappyBird.bird[birdID].jump = 17
                    flappyBird.bird[birdID].gravity = 5
                    flappyBird.bird[birdID].jumpSpeed = 10
        return 0

class savedBirds:
    def __init__(self,id):
        self.counter = 0
        self.id = id
        self.name = ""

class Bird:
    def __init__(self,id):
        self.id = id
        self.name = Players.names[id]
        self.color = Players.colors[id]
        self.positionX = distanceOfBirds * id + 70
        self.bird = pygame.Rect(self.positionX, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/"+str(id)+"_fly1.png").convert_alpha(),
                            pygame.image.load("assets/"+str(id)+"_fly2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.clickerID = Players.clickerIDs[id]
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((screenWidth, screenHeight))
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = wallSpawn
        self.counter = 1
        self.offset = random.randint(-110, 110)
        self.controller = Controller()
        self.deadBirds = [False for i in range(0,numberOfPlayers)]
        self.bird = [Bird(i) for i in range(0,numberOfPlayers)]
        self.savedBirds = [savedBirds(i) for i in range(0, numberOfPlayers)]
        self.walls = [Wall(i,self) for i in range(0,numberOfWalls)]

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(music)
        pygame.mixer.music.play(-1)





    def birdUpdate(self, birdID):
        if self.bird[birdID].jump:
            self.bird[birdID].jumpSpeed -= 1
            self.bird[birdID].birdY -= self.bird[birdID].jumpSpeed
            self.bird[birdID].jump -= 1
        else:
            self.bird[birdID].birdY += self.bird[birdID].gravity
            self.bird[birdID].gravity += 0.2
        self.bird[birdID].bird[1] = self.bird[birdID].birdY

        for i in range(0, numberOfWalls):
            if self.walls[i].upRect.colliderect(self.bird[birdID].bird):
                self.bird[birdID].dead = True
            if self.walls[i].downRect.colliderect(self.bird[birdID].bird):
                self.bird[birdID].dead = True
        if not 0 < self.bird[birdID].bird[1] < 720:
            self.deadBirds[birdID] = True
            self.bird[birdID].birdY = 800
            self.flag = False
            #check deadBirds array if every Bird is dead
            for i in range(0,numberOfPlayers):
                if(self.deadBirds[i] == False) :
                    self.flag = True
            #if every Bird is dead, reset
            if(self.flag == False) :
                for i in range(0,numberOfPlayers) :
                    if i == 1:
                        self.crash()
                    self.bird[i].bird[1] = 50
                    self.bird[i].birdY = 50
                    self.bird[i].dead = False
                    self.bird[i].counter = 0
                    self.bird[i].gravity = 5
                    self.deadBirds[i] = False
                for i in range(0, numberOfWalls):
                    self.walls[i].resetWalls()
                self.offset = random.randint(-110, 110)
                self.counter = 0

    def crash(self):
        fontBig = pygame.font.SysFont("Arial", 50,1)
        # insert highscore window, pause game till buttonpress
        global font
        displayScore = self.highscore() #score list of all birds




        flag = False
        counter = 0
        while not flag:
            if(useSensors == True):
                print self.controller.updateSensor(self)
            else:
                print self.controller.updateKeyboard(self)
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(fontBig.render("Highscores",
                                            -1,
                                            (0, 0, 0)),
                             (50, 20))
            for i in range(0, len(displayScore)):
                self.screen.blit(font.render(str(displayScore[i].counter),
                                             -1,
                                             (0, 0, 0)),
                                 (200, 100 * (i + 1)))
                self.screen.blit(font.render(str(displayScore[i].name),
                                             -1,
                                             (0, 0, 0)),
                                 (50, 100 * (i + 1)))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    flag = True
            if(useSensors == True):
                if self.controller.updateSensor(self):
                    flag = True
            else:
                if self.controller.updateKeyboard(self):
                    flag = True
            #display winning bird
            if counter<15:
                self.screen.blit(pygame.transform.scale(self.bird[displayScore[0].id].birdSprites[0],(200,200)), (400, 200))
            elif counter <30:
                self.screen.blit(pygame.transform.scale(self.bird[displayScore[0].id].birdSprites[1],(200,200)), (400, 200))
            else:
                counter = 0
            counter += 1
            pygame.display.update()

    def highscore(self):
        #copy all birds to savedBirds
        d = shelve.open('score.txt')  # here you will save the score variable
        #d['highscores'] = self.savedBirds
        currentScore = d['highscores']
        for i in range(0,len(self.savedBirds)):
            self.savedBirds[i].counter = self.bird[i].counter
            self.savedBirds[i].name = self.bird[i].name
            currentScore.append(self.savedBirds[i])

        currentScore = sorted(currentScore, key=operator.attrgetter('counter'), reverse=True)
        currentScore = currentScore[0:4]
        d['highscores'] = currentScore
        d.close()

        return currentScore

    def run(self):
        clock = pygame.time.Clock()
        global font
        while True:
            clock.tick(60)

            if(useSensors == True):
                self.controller.updateSensor(self)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
            else:
                self.controller.updateKeyboard(self)

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            for i in range(0, numberOfWalls):
                self.screen.blit(self.walls[i].wallUp,(self.walls[i].wallx, 360 + self.walls[i].gap - self.walls[i].offset))
                self.screen.blit(self.walls[i].wallDown,(self.walls[i].wallx, 0 - self.walls[i].gap - self.walls[i].offset))
            self.screen.blit(font.render(str(self.counter),
                           -1,
                            (255, 255, 255)),
                            (200, 50))
            for i in range(0,numberOfPlayers) :
                if self.bird[i].dead:
                    self.bird[i].sprite = 2
                elif self.bird[i].jump:
                    self.bird[i].sprite = 1
                self.screen.blit(self.bird[i].birdSprites[self.bird[i].sprite], (self.bird[i].positionX, self.bird[i].birdY))
                self.screen.blit(font.render(str(self.bird[i].name),
                                 -1,
                                 self.bird[i].color),
                                (self.bird[i].positionX, self.bird[i].birdY-50))
                if not self.bird[i].dead:
                    self.bird[i].sprite = 0
                self.birdUpdate(i)
            for i in range(0, numberOfWalls):
                self.walls[i].updateWallPosition()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
