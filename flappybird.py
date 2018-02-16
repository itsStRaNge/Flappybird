#!/usr/bin/env python

import pygame
import sys
import random
import shelve
import operator
import config
from wall import Wall
from controller import Controller
from birds import Bird, savedBirds

pygame.font.init()
font = pygame.font.SysFont(config.font['name'], config.font['size'])

class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.screenWidth,config.screenHeight))
        self.background = pygame.image.load("assets/background.png").convert()
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = 130
        self.wallx = config.wallSpawn
        self.counter = 1
        self.offset = random.randint(-110, 110)
        self.controller = Controller()
        self.deadBirds = [False for i in range(0,config.numberOfPlayers)]
        self.bird = [Bird(i) for i in range(0,config.numberOfPlayers)]
        self.savedBirds = [savedBirds(i) for i in range(0, config.numberOfPlayers)]
        self.walls = [Wall(i,self) for i in range(0,config.numberOfWalls)]

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(config.music)
        pygame.mixer.music.play(-1)

    def birdUpdate(self, birdID):
        if self.bird[birdID].jump:
            self.bird[birdID].jumpSpeed -= 1
            self.bird[birdID].positionY -= self.bird[birdID].jumpSpeed
            self.bird[birdID].jump -= 1
        else:
            self.bird[birdID].positionY += self.bird[birdID].gravity
            self.bird[birdID].gravity += 0.2
        self.bird[birdID].bird[1] = self.bird[birdID].positionY

        for i in range(0, config.numberOfWalls):
            if self.walls[i].upRect.colliderect(self.bird[birdID].bird):
                self.bird[birdID].dead = True
            if self.walls[i].downRect.colliderect(self.bird[birdID].bird):
                self.bird[birdID].dead = True

        if not 0 < self.bird[birdID].bird[1] < 720:
            self.deadBirds[birdID] = True
            self.bird[birdID].positionY = 800
            self.flag = False
            #check deadBirds array if every Bird is dead
            for i in range(0,config.numberOfPlayers):
                if(self.deadBirds[i] == False) :
                    self.flag = True

            #if every Bird is dead, reset
            if(self.flag == False) :
                for i in range(0,config.numberOfPlayers) :
                    if i == 1:
                        self.crash()
                    self.bird[i].bird[1] = 50
                    self.bird[i].positionY = 50
                    self.bird[i].dead = False
                    self.bird[i].counter = 0
                    self.bird[i].gravity = 5
                    self.deadBirds[i] = False
                for i in range(0, config.numberOfWalls):
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
            if(config.useSensors == True):
                #print self.controller.updateSensor(self)
                self.controller.updateSensor(self)
            else:
                #print self.controller.updateKeyboard(self)
                self.controller.updateKeyboard(self)
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

            if(config.useSensors == True):
                if self.controller.updateSensor(self, highscore_screen=True):
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
            clock.tick(30)

            if(config.useSensors == True):
                self.controller.updateSensor(self)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
            else:
                self.controller.updateKeyboard(self)

            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))
            for i in range(0, config.numberOfWalls):
                self.screen.blit(self.walls[i].wallUp,(self.walls[i].wallx, 360 + self.walls[i].gap - self.walls[i].offset))
                self.screen.blit(self.walls[i].wallDown,(self.walls[i].wallx, 0 - self.walls[i].gap - self.walls[i].offset))
            self.screen.blit(font.render(str(self.counter),
                           -1,
                            (255, 255, 255)),
                            (200, 50))
            for i in range(0,config.numberOfPlayers) :
                if self.bird[i].dead:
                    self.bird[i].sprite = 2
                elif self.bird[i].jump:
                    self.bird[i].sprite = 1
                self.screen.blit(self.bird[i].birdSprites[self.bird[i].sprite], (self.bird[i].positionX, self.bird[i].positionY))
                self.screen.blit(font.render(str(self.bird[i].name),
                                 -1,
                                 self.bird[i].color),
                                 (self.bird[i].positionX, self.bird[i].positionY - 50))
                if not self.bird[i].dead:
                    self.bird[i].sprite = 0
                self.birdUpdate(i)
            for i in range(0, config.numberOfWalls):
                self.walls[i].updateWallPosition()
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
