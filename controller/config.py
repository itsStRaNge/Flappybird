import serial
import pygame


useSensors = False

keys = [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_DOWN, pygame.K_UP]
click_ids = ['08af9020', '0c7e9e20']


serial = {
    'port': 'COM3',
    'baudrate': 57600,
    'parity': serial.PARITY_NONE,
    'stopbits': serial.STOPBITS_ONE,
    'bytesize': serial.EIGHTBITS,
    'timeout': 0
}