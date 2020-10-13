import sys

import pygame

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Game import Game
from Classes.Snake import Snake
from Classes.HostOrPlayerScreen import HostOrPlayerScreen
from Classes.WaitScreen import WaitSreen
from Classes.HostScreen import HostScreen
from Classes import consts

from Communication.receive import *

width = consts.WIDTH
height = consts.HEIGHT
speed = consts.SPEED

from tkinter import *
from tkinter import messagebox


def connect_to_host():
    host = ""
    close = None
    while host not in find_games():
        close, host = DataEnteringScreen('Initialization window', 'Enter host', width, height).run()
        if close:
            break
        if host not in find_games():
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('Host not found, try again', 'OK')

    if close is False and host is not None:
        #  по хосту подключаться, используй как хочешь
        close, name = DataEnteringScreen('What is your name?', 'Enter name', width, height).run()
        if close is False and name is not None:
            snakes = [Snake(name, width=width, height=height), Snake("test", width=width, height=height)]
            success, close_pressed, _ = WaitSreen().run()
            if close_pressed:
                sys.exit()
            elif success:
                # По идее, надо просто передать змейку хосту и там уже всё запускать
                Game(snakes, width=width, height=height, speed=speed).run()
            else:
                sys.exit()
        else:
            sys.exit()
    else:
        sys.exit()


def create_host():
    host = "Host"
    host_address = 'ABVD'
    res, _ = HostScreen('Your host data',
                        host_address, width,
                        height).run()
    create_game('ABVD')
    if res:
        r.flushdb()
        # вот здесь надо от юзеров получать змейки и кидать в массив
        snakes = [Snake(host, width=width, height=height), Snake("test", width=width, height=height)]

        Game(snakes, width=width, height=height).run()
    else:
        sys.exit()


def run():
    while True:
        # returns True if player else False . If something goes wrong - None
        hostOrGamer = HostOrPlayerScreen(width=width, height=height).run()

        if hostOrGamer is not None:
            if hostOrGamer:
                connect_to_host()
            else:
                create_host()
        else:
            break


run()
