#!/usr/bin/env python

import pygame
import random
import shelve
import operator
from wall.wall import Wall
from wall import config as wc
from controller import controller
from bird.bird import Bird, savedBirds
import config
import os

ABS_PATH = os.path.dirname(__file__)


class FlappyBird:
    def __init__(self):
        self.screen = pygame.display.set_mode((config.screenWidth, config.screenHeight))
        self.background = pygame.image.load(ABS_PATH + "/assets/background.png").convert()
        self.counter = 1
        self.offset = random.randint(-110, 110)
        self.bird_list = [Bird(i) for i in range(0, config.numberOfPlayers)]
        self.savedBirds = [savedBirds(i) for i in range(0, config.numberOfPlayers)]
        self.wall_list = [Wall(i, self) for i in range(0, wc.numberOfWalls)]

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(ABS_PATH + config.music)
        pygame.mixer.music.play(-1)
        pygame.font.init()
        self.font = pygame.font.SysFont(config.font['name'], config.font['size'])

        self.clock = pygame.time.Clock()

    def update_birds(self):

        all_dead_flag = True
        for bird in self.bird_list:
            for wall in self.wall_list:
                bird.dead = wall.collision(bird)
                # bird.update has to be after wall collision otherwise dead mechanism will be overwritten
                bird.update()
                if not bird.dead:
                    all_dead_flag = False

        # if every Bird is dead show highscore
        if all_dead_flag:
            self.highscore()

    def reset(self):
        self.bird_list = [Bird(i) for i in range(0, config.numberOfPlayers)]
        self.wall_list = [Wall(i, self) for i in range(0, wc.numberOfWalls)]
        self.counter = 0

    def highscore(self):
        fontBig = pygame.font.SysFont("Arial", 50, 1)
        # insert highscore window, pause game till buttonpress
        displayScore = [] #self.highscore() #score list of all birds

        while True:
            self.screen.blit(self.background, (0, 0))
            self.screen.blit(fontBig.render("Highscores",
                                            -1,
                                            (0, 0, 0)),
                             (50, 20))
            for i in range(0, len(displayScore)):
                self.screen.blit(self.font.render(str(displayScore[i].counter),
                                             -1,
                                             (0, 0, 0)),
                                 (200, 100 * (i + 1)))
                self.screen.blit(self.font.render(str(displayScore[i].name),
                                             -1,
                                             (0, 0, 0)),
                                 (50, 100 * (i + 1)))
            # display winning bird
            """if counter<15:
                self.screen.blit(pygame.transform.scale(self.bird_list[displayScore[0].id].birdSprites[0], (200, 200)), (400, 200))
            elif counter <30:
                self.screen.blit(pygame.transform.scale(self.bird_list[displayScore[0].id].birdSprites[1], (200, 200)), (400, 200))
            else:
                counter = 0
            counter += 1"""
            pygame.display.update()
            self.clock.tick(config.max_fps)

            if controller.check_input(self.bird_list):
                break
        self.reset()

    def get_highscore(self):
        # copy all birds to savedBirds
        d = shelve.open('score.txt')  # here you will save the score variable
        # d['highscores'] = self.savedBirds
        current_score = d['highscores']
        for i in range(0,len(self.savedBirds)):
            self.savedBirds[i].counter = self.bird_list[i].counter
            self.savedBirds[i].name = self.bird_list[i].name
            current_score.append(self.savedBirds[i])

        current_score = sorted(current_score, key=operator.attrgetter('counter'), reverse=True)
        current_score = current_score[0:4]
        d['highscores'] = current_score
        d.close()

        return current_score

    def run(self):
        while True:
            self.clock.tick(config.max_fps)

            controller.check_input(self.bird_list)

            # render background
            self.screen.fill((255, 255, 255))
            self.screen.blit(self.background, (0, 0))

            # render counter
            self.screen.blit(self.font.render(str(self.counter),
                             -1,
                             (255, 255, 255)),
                             (200, 50))
            # render walls
            for wall in self.wall_list:
                self.screen.blit(wall.wallUp, (wall.wall_x, 360 + wall.gap - wall.offset))
                self.screen.blit(wall.wallDown, (wall.wall_x, 0 - wall.gap - wall.offset))
                wall.update_wall_position()

            # render birds
            for bird in self.bird_list:
                self.update_birds()
                self.screen.blit(bird.birdSprites[bird.sprite], (bird.positionX, bird.positionY))
                self.screen.blit(self.font.render(str(bird.name),
                                 -1,
                                 bird.color),
                                 (bird.positionX, bird.positionY - 50))
            pygame.display.update()

if __name__ == "__main__":
    FlappyBird().run()
