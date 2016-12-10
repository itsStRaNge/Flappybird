#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random

numberOfPlayers = 1
screenWidth = 1200
numberOfWalls = 3



class Wall:
    def __init__(self, id):
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 150
        self.offset = random.randint(-110, 110)
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
        self.wallspeed = 2

    def offsetMovement(self):
        # self.offset = random.randint(-110, 110)
        if self.directionOfMovement == 1 and self.offset < 110:
            self.offset += 1

            if self.offset >= 110:
                self.directionOfMovement = 2

        elif self.directionOfMovement == 2:
            self.offset -= 1

            if self.offset <= -110:
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
            self.offset = random.randint(-110, 110)
            self.movementType = random.randint(1, 3)
            self.wallspeed += 0.2

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
        self.offset = random.randint(-110, 110)
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
        self.wallspeed = 2


class Bird:
    def __init__(self, id):
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.wallx = 350 + id * 50
        self.id = id
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((screenWidth, 720))
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.offset = random.randint(-110, 110)
        self.bird = [numberOfPlayers]
        self.walls = [Wall(i) for i in range(0,numberOfWalls)]
       # self.wall = Wall(0)
       # pygame.mixer.music.load('foo.mp3')
       # self.music.mixer.music.play(-1)

        for i in xrange(0, numberOfPlayers):
            self.bird[i] = Bird(i)






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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN) and not self.bird[
                    birdID].dead:  # or event.type == pygame.MOUSEBUTTONDOWN
                    if (event.key == K_UP):
                        self.bird[birdID].jump = 17
                        self.bird[birdID].gravity = 5
                        self.bird[birdID].jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            for i in range(0, numberOfWalls):
                self.screen.blit(self.walls[i].wallUp,(self.walls[i].wallx, 360 + self.walls[i].gap - self.walls[i].offset))
                self.screen.blit(self.walls[i].wallDown,(self.walls[i].wallx, 0 - self.walls[i].gap - self.walls[i].offset))
            self.screen.blit(font.render(str(self.bird[birdID].counter),-1,(255, 255, 255)),(200, 50))
            if self.bird[birdID].dead:
                self.bird[birdID].sprite = 2
                for i in range(0, numberOfWalls):
                    self.walls[i].resetWalls()
            elif self.bird[birdID].jump:
                self.bird[birdID].sprite = 1
            self.screen.blit(self.bird[birdID].birdSprites[self.bird[birdID].sprite], (70, self.bird[birdID].birdY))
            if not self.bird[birdID].dead:
                self.bird[birdID].sprite = 0
            #self.updateWalls()
            for i in range(0, numberOfWalls):
                self.walls[i].updateWallPosition()
            # maybe go throug array with id

            self.birdUpdate(birdID)
            pygame.display.update()


if __name__ == "__main__":
    FlappyBird().run()
