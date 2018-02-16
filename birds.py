import pygame
from player import Players
import config

class savedBirds:
    def __init__(self,id):
        self.counter = 0
        self.id = id
        self.name = ""

class Bird:
    def __init__(self,id):
        self.id = id
        self.name = Players.names[id]
        self.color = Players.colors[id]
        self.positionX = config.distanceOfBirds * id + 70
        self.bird = pygame.Rect(self.positionX, 50, 50, 50)
        self.birdSprites = [pygame.image.load("assets/"+str(id)+"_fly1.png").convert_alpha(),
                            pygame.image.load("assets/"+str(id)+"_fly2.png").convert_alpha(),
                            pygame.image.load("assets/dead.png")]
        self.positionY = config.start_y
        self.clickerID = Players.clickerIDs[id]
        self.dead = False
        self.sprite = 0
        self.jump = 0
        self.jumpSpeed = 10
        self.gravity = 10
        self.counter = 0