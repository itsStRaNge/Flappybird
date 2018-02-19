import config
import serial
import sys
import pygame


if config.useSensors:
    ser = serial.Serial(config.serial)


def check_input(bird_list):
    if config.useSensors:
        return input_sensor(bird_list)
    else:
        return input_keyboard(bird_list)


def input_sensor(bird_list):
    num_bytes_input_buf = ser.inWaiting()
    if num_bytes_input_buf >= 32:
        rcv_bytes = ser.read(32)
        clicker_id = rcv_bytes[9:13]
        clicker_state = rcv_bytes[7]

        if clicker_state.encode('hex') == '10':
            print clicker_id.encode('hex')
            for bird in bird_list:
                if bird.clickerID == clicker_id.encode('hex'):
                    bird.jump_trigger()
                    return True
    return False


def input_keyboard(bird_list):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            for bird in bird_list:
                if event.key == bird.key:
                    bird.jump_trigger()
                    return True
    return False
