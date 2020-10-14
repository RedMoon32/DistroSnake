from threading import Thread

import keyboard as keyboard

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Game import Game
from Classes.Snake import Snake
from Classes.HostOrPlayerScreen import HostOrPlayerScreen
from Classes.WaitScreen import WaitSreen
from Classes.HostScreen import HostScreen
from Communication.receive import *

width = consts.WIDTH
height = consts.HEIGHT
speed = consts.SPEED

from tkinter import *
from tkinter import messagebox

set_alive_thread = None

name = 'HOST'
val = True


def set_alive():
    while True:
        if name:
            set_key(name, val, ex=1)


def play(host):
    while True:
        global val
        res = Game.game_calculate_once(host)
        val = res


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
                play(host=host)
            else:
                sys.exit()


def create_host():
    game_name = 'ABVD'
    create_game(game_name)
    res, _ = HostScreen('Your host data',
                        game_name, width,
                        height).run(game_name)
    # вот здесь надо от юзеров получать змейки и кидать в массив
    # По идее, надо просто передать змейку хосту и там уже всё запускать

    snakes = [Snake(name, width=width, height=height) for name in get_game(game_name)["snakes"]]
    game = Game(snakes, width=width, height=height, speed=speed)
    update_game_var(game_name, "state", game.to_dict())
    update_game_var(game_name, "status", PLAYING)
    play(host=game_name)


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


def listen():
    return
    global val
    while True:  # making a loop
        if keyboard.is_pressed('d'):
            val = "RIGHT"
        elif keyboard.is_pressed('a'):
            val = "LEFT"
        elif keyboard.is_pressed('w'):
            val = "UP"
        elif keyboard.is_pressed('s'):
            val = "DOWN"


if __name__ == "__main__":
    thread = Thread(target=set_alive, )
    thread2 = Thread(target=listen, )
    thread2.daemon = True
    thread2.start()
    thread.daemon = True
    thread.start()
    run()
