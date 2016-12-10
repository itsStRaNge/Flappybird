#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random


class Bird:
    def __init__(self):
        self.bird = pygame.Rect(65, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/1.png").convert_alpha(),
                            pygame.image.load("assets/2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.dead = False
        
class FlappyBird:
    def __init__(self):
        #self.screen = pygame.display.set_mode((800, 708))
        self.screen = pygame.display.set_mode((640,480),pygame.FULLSCREEN)
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = 400
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
 
        self.sprite = 0
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.bird = Bird()

    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = 400
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.dead.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.bird.birdY += self.gravity
            self.gravity += 0.2
        self.bird.bird[1] = self.bird.birdY
        upRect = pygame.Rect(self.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.dead.bird):
            self.dead.dead = True
        if downRect.colliderect(self.dead.bird):
            self.dead.dead = True
        if not 0 < self.bird[1] < 720:
            self.dead.bird[1] = 50
            self.dead.birdY = 50
            self.dead.dead = False
            self.counter = 0
            self.wallx = 400
            self.offset = random.randint(-110, 110)
            self.gravity = 5

    def run(self):
        clock = pygame.time.Clock()
        pygame.font.init()
        font = pygame.font.SysFont("Arial", 50)
        while True:
            clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN) and not self.dead.dead:
                    self.jump = 17
                    self.gravity = 5
                    self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.dead.dead:
                self.dead.sprite = 2
            elif self.jump:
                self.dead.sprite = 1
            self.screen.blit(self.dead.birdSprites[self.dead.sprite], (70, self.dead.birdY))
            if not self.dead.dead:
                self.dead.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
