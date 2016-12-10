#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import serial

class Controller:
    def __init__(self):
        self.ser = serial.Serial(
            port='/dev/ttyAMA0',
            baudrate = 9600,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,
            timeout=0
        )
    def update(self,flappyBird):
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
            


numberOfPlayers = 3
wallSpawn = 1000
distanceOfBirds = 126
clickerIDs = ["01a7fd15","01a7fe21","01a7c30b"]
names = ["nico","clemens","luis","jakob"]

class Bird:
    def __init__(self,id):
        self.id = id
        self.name = names[id]
        self.positionX = distanceOfBirds * id + 70
        self.bird = pygame.Rect(self.positionX, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.clickerID = clickerIDs[id]
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0
        
class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((1000,600))
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

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = wallSpawn
            self.bird[0].counter += 1
            self.offset = random.randint(-110, 110)
            self.counter += 1

    def birdUpdate(self,birdID):
        if self.bird[birdID].jump:
            self.bird[birdID].jumpSpeed -= 1
            self.bird[birdID].birdY -= self.bird[birdID].jumpSpeed
            self.bird[birdID].jump -= 1
        else:
            self.bird[birdID].birdY += self.bird[birdID].gravity
            self.bird[birdID].gravity += 0.2
        self.bird[birdID].bird[1] = self.bird[birdID].birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird[birdID].bird):
            self.bird[birdID].dead = True
        if downRect.colliderect(self.bird[birdID].bird):
            self.bird[birdID].dead = True
        if not 0 < self.bird[birdID].bird[1] < 720:
            self.deadBirds[birdID] = True
            self.flag = False
            #check deadBirds array if every Bird is dead
            for i in range(0,numberOfPlayers):
                if(self.deadBirds[i] == False) :
                    self.flag = True
            #if every Bird is dead, reset
            if(self.flag == False) :
                for i in range(0,numberOfPlayers) :
                    self.bird[i].bird[1] = 50
                    self.bird[i].birdY = 50
                    self.bird[i].dead = False
                    self.bird[i].counter = 0
                    self.bird[i].gravity = 5
                    self.deadBirds[i] = False
                self.wallx = wallSpawn
                self.offset = random.randint(-110, 110)
                self.counter = 0

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
       
        while True:
            clock.tick(60)

            self.controller.update(self)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                (self.wallx, 0 - self.gap - self.offset))
            #maybe global counter and safe if dies
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
                if not self.bird[i].dead:
                    self.bird[i].sprite = 0
                self.updateWalls()
                self.birdUpdate(i)               
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
