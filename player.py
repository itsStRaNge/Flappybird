import pygame
import config
class Players:
    clickerIDs = config.click_ids
    keys = [pygame.K_RIGHT,pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]
    names = config.names
    colors = [(0,0,255),(0,255,0),(255,0,0),(120,0,120)]