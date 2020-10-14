from threading import Thread
from time import sleep

from Classes.DataEnteringScreen import DataEnteringScreen
from Test.TestGame import TestGame
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

name = 'HOST'


def set_alive():
    while True:
        if name:
            set_key(name, True, ex=2)
            sleep(1)


def connect_to_host():
    host = "ABVD"
    while host not in find_games():
        host = DataEnteringScreen('Initialization window', 'Enter host', width, height).run()
        if host not in find_games():
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('Error', 'Host not found, try again')
    global name
    if host is not None:
        #  по хосту подключаться, используй как хочешь
        name = None
        name = "OK"
        while not name:
            name = DataEnteringScreen('What is your name?', 'Enter non empty name', width, height).run()

        connect_to_game(host, name)

        if name is not None:

            success = WaitSreen().run(host)
            if success:
                while True:
                    res = get_game(host)["state"]
                    game = TestGame.from_dict(res)
                    game.render()
            else:
                sys.exit()


def create_host():
    host = "Host"
    game_name = 'ABVD'
    create_game(game_name)
    res, _ = HostScreen('Your host data',
                        game_name, width,
                        height).run(game_name)
    # вот здесь надо от юзеров получать змейки и кидать в массив
    # По идее, надо просто передать змейку хосту и там уже всё запускать

    snakes = [Snake(name, width=width, height=height), Snake("test", width=width, height=height)]
    game = TestGame(snakes, width=width, height=height, speed=speed)
    update_game_var(game_name, "status", PLAYING)
    game.run()


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


if __name__ == "__main__":
    thread = Thread(target=set_alive, )
    thread.daemon = True
    thread.start()
    run()