import pygame
import config
from controller import config as cc
from game import config as gc
import os

ABS_PATH = os.path.dirname(__file__)

class savedBirds:
    def __init__(self, id):
        self.counter = 0
        self.id = id
        self.name = ""


class Bird:
    def __init__(self, id):
        self.id = id
        self.name = gc.names[id]
        self.color = gc.colors[id]
        self.key = cc.keys[id]
        self.positionX = config.distanceOfBirds * id + 70
        self.hit_box = pygame.Rect(self.positionX, 50, 50, 50)
        self.birdSprites = [pygame.image.load(ABS_PATH + "/assets/%s_fly1.png" % id).convert_alpha(),
                            pygame.image.load(ABS_PATH + "/assets/%s_fly2.png" % id).convert_alpha(),
                            pygame.image.load(ABS_PATH + "/assets/dead.png")]
        self.positionY = config.start_y
        self.clickerID = cc.click_ids[id]
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = config.jump_speed
        self.gravity = gc.gravity_start
        self.counter = 0

    def jump_trigger(self):
        if not self.dead:
            self.jump = config.jump
            self.gravity = gc.gravity_start
            self.jumpSpeed = config.jump_speed

    def update(self):
        if self.jump:
            self.jumpSpeed -= config.jump_speed_gain
            self.positionY -= self.jumpSpeed
            self.jump -= config.jump_gain
        else:
            self.positionY += self.gravity
            self.gravity += gc.gravity_gain
        self.hit_box[1] = self.positionY

        if not 0 < self.hit_box[1] < gc.screenHeight:
            self.dead = True
            self.positionY = gc.screenHeight + 200
        self.select_sprite()

    def select_sprite(self):
        if self.dead:
            self.sprite = 2
        elif self.jump:
            self.sprite = 1
        else:
            self.sprite = 0
