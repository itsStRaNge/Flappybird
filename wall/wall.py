import pygame
import random
import config
from game import config as gc
import os

ABS_PATH = os.path.dirname(__file__)


class Wall:
    def __init__(self, id, flappy_bird):
        self.wallUp = pygame.image.load(ABS_PATH + "/assets/bottom.png").convert_alpha()
        self.wallDown = pygame.image.load(ABS_PATH + "/assets/top.png").convert_alpha()
        self.gap = config.gap
        self.offset = random.randint(-(gc.screenHeight*0.2), gc.screenHeight*0.4)
        self.id = id
        self.wall_x = gc.screenWidth + self.id * gc.screenWidth / config.numberOfWalls
        self.upRect = pygame.Rect(self.wall_x,
                                  config.wall_up_spawn + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wall_x,
                                    config.wall_down_spawn - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())
        self.movementType = 1
        self.directionOfMovement = 1
        self.wall_speed = 6
        self.flappybird = flappy_bird

    def offset_movement(self):
        if self.directionOfMovement == 1 and self.offset < gc.screenHeight*0.4:
            self.offset += 1

            if self.offset >= -(gc.screenHeight*0.2):
                self.directionOfMovement = 2

        elif self.directionOfMovement == 2:
            self.offset -= 1

            if self.offset <=  -(gc.screenHeight*0.2):
                self.directionOfMovement = 1

    def update_gap(self):
        if self.directionOfMovement == 2 and self.gap < 200:
            self.gap += 4

            if self.gap >= 200:
                self.directionOfMovement = 1

        elif self.directionOfMovement == 1:
            self.gap -= 4

            if self.gap <= 150:
                self.directionOfMovement = 2

    def update_wall_position(self):
        self.wall_x -= self.wall_speed

        if self.wall_x < -80:
            self.wall_x = gc.screenWidth
            self.offset = random.randint(-(gc.screenHeight*0.2), gc.screenHeight*0.4)
            self.movementType = random.randint(1, 3)
            self.wall_speed += 0.2
            self.flappybird.counter += 1
            for bird in self.flappybird.bird_list:
                if not bird.dead:
                    bird.counter += 1

        if self.movementType == 2:
            self.update_gap()
        elif self.movementType == 3:
            self.offset_movement()
        self.upRect = pygame.Rect(self.wall_x,
                                  config.wall_up_spawn + self.gap - self.offset + 10,
                                  self.wallUp.get_width() - 10,
                                  self.wallUp.get_height())
        self.downRect = pygame.Rect(self.wall_x,
                                    config.wall_down_spawn - self.gap - self.offset - 10,
                                    self.wallDown.get_width() - 10,
                                    self.wallDown.get_height())

    def collision(self, bird):
        if self.upRect.colliderect(bird.hit_box):
            return True
        if self.downRect.colliderect(bird.hit_box):
            return True
