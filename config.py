import pygame

useSensors = True
screenWidth = 1000
screenHeight = 600
music = "music/main.mp3"
font = {'name':"Arial", 'size':30}

# player config
numberOfPlayers = 2
click_ids = ['08af9020','0c7e9e20']#["a7f0c920", "a7f4ef20", "a7f8bf20", "a7effa20"]
names = ["Felix", "Clemens", "Jakob", "Luis"]

# bird config
start_y = 200
distanceOfBirds = 126

# wall config
gap = 220
numberOfWalls = 2
wallSpawn = 1000
wall_up_spawn = 360
wall_down_spawn = 0