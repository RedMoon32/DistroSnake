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

set_alive_thread = None


def connect_to_host():
    host = None
    while host not in find_games():
        host = DataEnteringScreen('Initialization window', 'Enter host', width, height).run()
        if host not in find_games():
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('Error', 'Host not found, try again')

    if host is not None:
        #  по хосту подключаться, используй как хочешь
        name = None
        while not name:
            name = DataEnteringScreen('What is your name?', 'Enter non empty name', width, height).run()

        connect_to_game(host, name)

        if name is not None:
            snakes = [Snake(name, width=width, height=height), Snake("test", width=width, height=height)]
            success, _ = WaitSreen().run(host)
            if success:
                # По идее, надо просто передать змейку хосту и там уже всё запускать
                Game(snakes, width=width, height=height, speed=speed).run()
            else:
                sys.exit()


def create_host():
    host = "Host"
    host_address = 'ABVD'
    create_game(host_address)
    res, _ = HostScreen('Your host data',
                        host_address, width,
                        height).run(host_address)
    # вот здесь надо от юзеров получать змейки и кидать в массив
    snakes = [Snake(host, width=width, height=height), Snake("test", width=width, height=height)]

    Game(snakes, width=width, height=height).run()


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
