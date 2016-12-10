#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import serial

ser = serial.Serial(

        port='/dev/ttyAMA0',
        baudrate = 9600,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.EIGHTBITS,
        timeout=0
)

numberOfPlayers = 1

class Bird:
    def __init__(self,id):
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.wallx = 350 + id* 50
        self.id = id
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0
        
class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((640,480))
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.offset = random.randint(-110, 110)
        self.bird = [numberOfPlayers]
        for i in xrange(0,numberOfPlayers):
            self.bird[i] = Bird(i)
        
    def updateWalls(self):
        self.bird[0].wallx -= 2
        if self.bird[0].wallx < -80:
            self.bird[0].wallx = 350 + 50 * self.bird[0].id
            self.bird[0].counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self,birdID):
        if self.bird[birdID].jump:
            self.bird[birdID].jumpSpeed -= 1
            self.bird[birdID].birdY -= self.bird[birdID].jumpSpeed
            self.bird[birdID].jump -= 1
        else:
            self.bird[birdID].birdY += self.bird[birdID].gravity
            self.bird[birdID].gravity += 0.2
        self.bird[birdID].bird[1] = self.bird[birdID].birdY
        upRect = pygame.Rect(self.bird[birdID].wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.bird[birdID].wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird[birdID].bird):
            self.bird[birdID].dead = True
        if downRect.colliderect(self.bird[birdID].bird):
            self.bird[birdID].dead = True
        if not 0 < self.bird[birdID].bird[1] < 720:
            self.bird[birdID].bird[1] = 50
            self.bird[birdID].birdY = 50
            self.bird[birdID].dead = False
            self.bird[birdID].counter = 0
            self.bird[birdID].wallx = 350 + 50 * self.bird[birdID].id
            self.offset = random.randint(-110, 110)
            self.bird[birdID].gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        birdID = 0
        while True:
            clock.tick(60)
            
            bytesWaiting = ser.inWaiting()
            if bytesWaiting == 14:
                x=ser.read(14)
                en_id = x[8:12]
                state = x[4]
                
                if state.encode('hex') == '10' and not self.bird[birdID].dead:
                    self.bird[birdID].jump = 17
                    self.bird[birdID].gravity = 5
                    self.bird[birdID].jumpSpeed = 10

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.bird[birdID].wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.bird[birdID].wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.bird[birdID].counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.bird[birdID].dead:
                self.bird[birdID].sprite = 2
            elif self.bird[birdID].jump:
                self.bird[birdID].sprite = 1
            self.screen.blit(self.bird[birdID].birdSprites[self.bird[birdID].sprite], (70, self.bird[birdID].birdY))
            if not self.bird[birdID].dead:
                self.bird[birdID].sprite = 0
            self.updateWalls()
            #maybe go throug array with id
            
            self.birdUpdate(birdID)
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
