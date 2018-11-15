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
        self.sprite = 0
        self.dead = False
        self.jump = False
        self.counter = 0
        self.velocity = 0
        self.acceleration = 0

    def jump_trigger(self):
        if not self.dead:
            self.acceleration = 0
            self.velocity = config.jump_velocity
            self.jump = True

    def update(self):

        self.positionY -= self.calculate_movement()

        print("y = %s | v = %s | a = %s" % (self.positionY, self.velocity, self.acceleration))

        self.hit_box[1] = self.positionY

        if not 0 < self.hit_box[1] < gc.screenHeight:
            self.dead = True
            self.positionY = gc.screenHeight + 200
        self.select_sprite()

    def calculate_movement(self):
        if abs(self.velocity) < config.velocity_max:
            if self.jump and self.velocity < 0:
                self.acceleration = 0
                self.jump = False
            self.acceleration -= gc.gravity_acceleration
            self.velocity += self.acceleration
        else:
            self.velocity = config.velocity_max * (self.velocity / abs(self.velocity))
        return self.velocity

    def select_sprite(self):
        if self.dead:
            self.sprite = 2
        elif self.jump:
            self.sprite = 1
        else:
            self.sprite = 0
