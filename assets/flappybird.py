#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random


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
        
class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((640,480))
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0
        self.offset = random.randint(-110, 110)
        self.bird = Bird(1)
		

    def updateWalls(self):
        self.bird.wallx -= 2
        if self.bird.wallx < -80:
            self.bird.wallx = 350 + 50 * self.bird.id
            self.counter += 1
            self.offset = random.randint(-110, 110)

    def birdUpdate(self):
        if self.jump:
            self.jumpSpeed -= 1
            self.bird.birdY -= self.jumpSpeed
            self.jump -= 1
        else:
            self.bird.birdY += self.gravity
            self.gravity += 0.2
        self.bird.bird[1] = self.bird.birdY
        upRect = pygame.Rect(self.bird.wallx,
                             360 + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        downRect = pygame.Rect(self.bird.wallx,
                               0 - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        if upRect.colliderect(self.bird.bird):
            self.bird.dead = True
        if downRect.colliderect(self.bird.bird):
            self.bird.dead = True
        if not 0 < self.bird.bird[1] < 720:
            self.bird.bird[1] = 50
            self.bird.birdY = 50
            self.bird.dead = False
            self.counter = 0
            self.bird.wallx = 350 + 50 * self.bird.id
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
                if (event.type == pygame.KEYDOWN ) and not self.bird.dead: #or event.type == pygame.MOUSEBUTTONDOWN
                    if(event.key == K_UP) :
                        self.jump = 17
                        self.gravity = 5
                        self.jumpSpeed = 10

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(self.wallUp,
                             (self.bird.wallx, 360 + self.gap - self.offset))
            self.screen.blit(self.wallDown,
                             (self.bird.wallx, 0 - self.gap - self.offset))
            self.screen.blit(font.render(str(self.counter),
                                         -1,
                                         (255, 255, 255)),
                             (200, 50))
            if self.bird.dead:
                self.bird.sprite = 2
            elif self.jump:
                self.bird.sprite = 1
            self.screen.blit(self.bird.birdSprites[self.bird.sprite], (70, self.bird.birdY))
            if not self.bird.dead:
                self.bird.sprite = 0
            self.updateWalls()
            self.birdUpdate()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
