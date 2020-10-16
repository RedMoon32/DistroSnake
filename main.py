import random
import string
from threading import Thread

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Game import Game
from Classes.Snake import Snake
from Classes.HostOrPlayerScreen import HostOrPlayerScreen
from Classes.WaitScreen import WaitSreen
from Classes.HostScreen import HostScreen
from Communication.communication_consts import PLAYING
from Communication.receive import *

width = consts.WIDTH
height = consts.HEIGHT
speed = consts.SPEED

from tkinter import *
from tkinter import messagebox

set_alive_thread = None
name = "HOST"
val = True
stop_sign = False
loc_redis = '-'
sum = 0
frame_cont = 0
count = 1
dirs = ["DOWN", "RIGHT", "UP", "LEFT"]
real_dirs = [dir for dir in dirs for i in range(count)]
a = iter(itertools.cycle(real_dirs))


def set_alive():
    while not stop_sign:
        if name:
            set_key(name, loc_redis, ex=1)


def play(host, player_name):
    import time

    global stop_sign
    stop_sign = True
    while True:
        global sum, frame_cont, val
        start = time.time()

        res = Game.game_calculate_once(host, player_name)
        # res = next(a)

        setted = set_key(name, val)

        if res:
            val = res


def connect_to_host():
    host = None
    while host not in find_games():
        host = DataEnteringScreen(
            "Initialization window", "Enter host", width, height
        ).run()
        if host not in find_games():
            Tk().wm_withdraw()  # tozz hide the main window
            messagebox.showinfo("Error", "Host not found, try again")
    global name
    if host is not None:
        #  по хосту подключаться, используй как хочешь
        name = None
        while not name:
            name = DataEnteringScreen(
                "Enter nickname", "Enter nickname?", width, height
            ).run()

        connect_to_game(host, name)

        if name is not None:

            success = WaitSreen().run(host)
            if success:
                play(host=host, player_name=name)
            else:
                sys.exit()


def body_choice(ind, w, h):
    # left up corner, goes down
    if ind == 0:
        return [[50, 50], [50, 40], [50, 30]], "DOWN"

    # left down corner, goes right
    elif ind == 1:
        return [[70, h - 50], [60, h - 50], [50, h - 50]], "RIGHT"

    # right down corner, moves up
    elif ind == 2:
        return [[w - 50, h - 50], [w - 40, h - 50], [w - 30, h - 50]], "UP"

    # right upper corner, moves left
    elif ind == 3:
        return [[w - 50, 30], [w - 50, 40], [w - 50, 50]], "LEFT"
    else:
        return None, None


def create_host():
    game_name = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(5))
    game_name = "abvd"
    create_game(game_name)
    res, _ = HostScreen("Your host data", game_name, width, height).run(game_name)
    # вот здесь надо от юзеров получать змейки и кидать в массив
    # По идее, надо просто передать змейку хосту и там уже всё запускать
    snakes = [
        Snake(name, width=width, height=height)
        for name in get_game(game_name)["snakes"]
    ]
    for ind, snake in enumerate(snakes):
        body, direction = body_choice(ind, width, height)
        if body is not None and direction is not None:
            snake.body = body
            snake.head_pos = body[0]
            snake.direction = direction

    game = Game(snakes, width=width, height=height, speed=speed, host_addr=game_name)
    game.scores = [0 for i in game.scores]
    update_game_var(game_name, "state", game.to_dict())
    update_game_var(game_name, "status", PLAYING)
    play(host=game_name, player_name="HOST")


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


def game_init():
    import sys
    global loc_redis
    count_args = len(sys.argv) - 1
    if count_args == 4:
        mip, mport, iip, iport = sys.argv[1:]

    elif count_args == 2:
        mip, mport = sys.argv[1], sys.argv[2]
        iip, iport = None, None

    elif count_args == 3 and sys.argv[3] == "-i":
        mip, mport = sys.argv[1], sys.argv[2]
        iip, iport = mip, mport

    else:
        print(
            "Wrong argument passing, please run the script using following command:\npython snake.py "
            "<master ip in local network> <master redis port in local network> (-i if is master) "
            "<your ip in local network> <your open redis port>")
        sys.exit(-1)

    try:
        cl = set_client(mip, mport)
        if iip and iport:
            loc_redis = [iip, iport]
            Redis(iip, iport).flushdb()
            print("Flushed own redis storage")

            print("Connected to redis ",cl)
    except:
        print("Error connecting to local Redis Instance")
        sys.exit(-1)

    thread = Thread(
        target=set_alive,
    )
    flush_dbs()
    thread.daemon = True
    thread.start()
    run()


if __name__ == "__main__":
    game_init()
