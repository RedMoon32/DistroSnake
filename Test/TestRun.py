from threading import Thread
from time import sleep

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

name = 'HOST'


def set_alive():
    while True:
        print('Set Alive')
        set_key(name, True, ex=100)
        sleep(1)


def connect_to_host():
    host = None
    while host not in find_games():
        host = DataEnteringScreen('Initialization window', 'Enter host', width, height).run()
        if host not in find_games():
            Tk().wm_withdraw()  # to hide the main window
            messagebox.showinfo('Error', 'Host not found, try again')
    global name
    if host is not None:
        #  по хосту подключаться, используй как хочешь
        name = None
        while not name:
            name = DataEnteringScreen('What is your name?', 'Enter non empty name', width, height).run()

        connect_to_game(host, name)

        if name is not None:
            goes_down_snake = Snake(name="downer", width=width, height=height, head_pos=[10, 10],
                                    body=[[20, 10], [30, 10]]
                                    , direction="DOWN", alive=True, died_from_self=False, died_from_snake=False,
                                    died_from_wall=False)

            goes_right_snake = Snake(name="righter", width=width, height=height, head_pos=[60, 60],
                                     body=[[50, 60], [40, 60]]
                                     , direction="RIGHT", alive=True, died_from_self=False, died_from_snake=False,
                                     died_from_wall=False)
            snakes = [goes_down_snake, goes_right_snake]

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
    goes_down_snake = Snake(name="downer", width=width, height=height, head_pos=[10, 10], body=[[10, 10],[20, 10], [30, 10]]
                            , direction="DOWN", alive=True, died_from_self=False, died_from_snake=False,
                            died_from_wall=False)

    goes_right_snake = Snake(name="righter", width=width, height=height, head_pos=[60, 60], body=[[60, 60],[50, 60], [40, 60]]
                             , direction="RIGHT", alive=True, died_from_self=False, died_from_snake=False,
                             died_from_wall=False)
    snakes = [goes_down_snake, goes_right_snake]

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


if __name__ == "__main__":
    # thread = Thread(target=set_alive, )
    # thread.daemon = True
    # thread.start()
    run()
