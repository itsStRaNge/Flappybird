import config
import serial
import sys
from player import Players
import pygame

class Controller:
    def __init__(self):
        if(config.useSensors == True):
            self.ser = serial.Serial(
                port='COM3',
                baudrate = 57600,
                parity=serial.PARITY_NONE,
                stopbits=serial.STOPBITS_ONE,
                bytesize=serial.EIGHTBITS,
                timeout=0
            )

    def updateSensor(self,flappyBird, highscore_screen=False):
        numberOfBytesInInputBuffer = self.ser.inWaiting()
        if numberOfBytesInInputBuffer >= 32:
            receivedBytes = self.ser.read(32)
            clickerID = receivedBytes[9:13]
            clickerState = receivedBytes[7]

            if clickerState.encode('hex') == '10':
                print clickerID.encode('hex')
                if highscore_screen:
                    return 1
                for birdID in range(0,config.numberOfPlayers):
                    if flappyBird.bird[birdID].clickerID == clickerID.encode('hex') and not flappyBird.bird[birdID].dead:
                        flappyBird.bird[birdID].jump = 17
                        flappyBird.bird[birdID].gravity = 5
                        flappyBird.bird[birdID].jumpSpeed = 10
                        return 0
                    elif flappyBird.bird[birdID].clickerID == clickerID.encode('hex') and flappyBird.bird[birdID].dead:
                        return 1
        return 0

    def updateKeyboard(self,flappyBird):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if (event.type == pygame.KEYDOWN):  # and not self.bird[birdID].dead
                birdID = -1
                if (event.key == Players.keys[0]):
                    birdID = 0
                elif (event.key == Players.keys[1]):
                    birdID = 1
                elif (event.key == Players.keys[2]):
                    birdID = 2
                elif (event.key == Players.keys[3]):
                    birdID = 3
                if (birdID != -1 and birdID < config.numberOfPlayers and not flappyBird.bird[birdID].dead):
                    flappyBird.bird[birdID].jump = 17
                    flappyBird.bird[birdID].gravity = 5
                    flappyBird.bird[birdID].jumpSpeed = 10
        return 0
