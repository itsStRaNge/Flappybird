import pygame
import random
import config

class Wall:
    def __init__(self, id, flappybird):
        self.wallUp = pygame.image.load("assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load("assets/top.png").convert_alpha()
        self.gap = config.gap
        self.offset = random.randint(-(config.screenHeight*0.2), config.screenHeight*0.4)
        self.id = id
        self.wallx = config.screenWidth+ self.id*config.screenWidth/config.numberOfWalls
        self.upRect = pygame.Rect(self.wallx,
                             config.wall_up_spawn + self.gap - self.offset + 10,
                             self.wallUp.get_width() - 10,
                             self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                               config.wall_down_spawn - self.gap - self.offset - 10,
                               self.wallDown.get_width() - 10,
                               self.wallDown.get_height())
        self.movementType = 1
        self.directionOfMovement = 1
        self.wallspeed = 6
        self.flappybird = flappybird

    def offsetMovement(self):
        if self.directionOfMovement == 1 and self.offset < config.screenHeight*0.4:
            self.offset += 1

            if self.offset >= -(config.screenHeight*0.2):
                self.directionOfMovement = 2

        elif self.directionOfMovement == 2:
            self.offset -= 1

            if self.offset <=  -(config.screenHeight*0.2):
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
            self.wallx = config.screenWidth
            self.offset = random.randint(-(config.screenHeight*0.2), config.screenHeight*0.4)
            self.movementType = random.randint(1, 3)
            self.wallspeed += 0.2
            self.flappybird.counter += 1
            for i in range(0,config.numberOfPlayers):
                if not self.flappybird.bird[i].dead:
                    self.flappybird.bird[i].counter += 1

        if self.movementType == 2:
            self.updateGap()
        elif self.movementType == 3:
            self.offsetMovement()
        self.upRect = pygame.Rect(self.wallx,
                                  config.wall_up_spawn + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                                    config.wall_down_spawn - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())

    def resetWalls(self):
        self.gap = 150
        self.offset =  random.randint(-(config.screenHeight*0.2), config.screenHeight*0.4)
        self.wallx = config.screenWidth+ self.id*config.screenWidth/config.numberOfWalls
        self.upRect = pygame.Rect(self.wallx,
                                  config.wall_up_spawn + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wallx,
                                    config.wall_down_spawn - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())
        self.movementType = 1
        self.directionOfMovement = 1
        self.wallspeed = 6
        self.flappybird.counter = 0