#!/usr/bin/env python

import pygame
from pygame.locals import *  # noqa
import sys
import random
import shelve
import operator
numberOfPlayers = 2
wallSpawn = 1000
distanceOfBirds = 126
keys = [K_LEFT,K_RIGHT,K_UP,K_DOWN]
names = ["nico","clemens","luis","jakob"]

pygame.font.init()
font = pygame.font.SysFont("Arial", 30)

class savedBirds:
    def __init__(self,id):
        self.counter = 0
        self.id = id
        self.name = ""
class Bird:
    def __init__(self,id):
	self.id = id
	self.name = names[id]
        self.positionX = distanceOfBirds * id + 70
        self.bird = pygame.Rect(self.positionX, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/"+str(id)+"_fly1.png").convert_alpha(),
                            pygame.image.load("assets/"+str(id)+"_fly2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.birdY = 350
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0
        self.key = keys[id]
        
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
        self.deadBirds = [False for i in range(0,numberOfPlayers)]
        self.bird = [Bird(i) for i in range(0,numberOfPlayers)]

        self.savedBirds = [savedBirds(i) for i in range(0, numberOfPlayers)]
    def updateWalls(self):
        self.wallx -= 2
        if self.wallx < -80:
            self.wallx = wallSpawn
            self.bird[0].counter += 1
            self.offset = random.randint(-110, 110)
            self.counter += 1
            for i in range(0,numberOfPlayers):
                if(self.deadBirds[i] == False):
                    self.bird[i].counter = self.counter

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
                    self.crash()
                    self.bird[i].bird[1] = 50
                    self.bird[i].birdY = 50
                    self.bird[i].dead = False
                    self.bird[i].counter = 0
                    self.bird[i].gravity = 5
                    self.deadBirds[i] = False
                self.wallx = wallSpawn
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
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if (event.type == pygame.KEYDOWN ) : #and not self.bird[birdID].dead
                    birdID = -1
                    if(event.key == keys[0]) :
                        birdID = 0
                    elif (event.key == keys[1]) :
                        birdID = 1
                    elif (event.key == keys[2]) :
                        birdID = 2
                    elif (event.key == keys[3]) :
                        birdID = 3
                    if(birdID != -1 and birdID < numberOfPlayers and not self.bird[birdID].dead) :
                        self.bird[birdID].jump = 17
                        self.bird[birdID].gravity = 5
                        self.bird[birdID].jumpSpeed = 10

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
