from threading import Thread

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


sum = 0
frame_cont = 0


def play(host, player_name):
    import time
    while True:
        global sum, frame_cont, val
        start = time.time()

        res = Game.game_calculate_once(host, player_name)

        end = time.time()
        cur_ = (start - end)
        sum += cur_
        frame_cont += 1
        mean = sum / frame_cont
        if cur_ < mean:
            print('less')
            time.sleep(mean - cur_)

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
    game_name = 'ABVD'
    create_game(game_name)
    res, _ = HostScreen('Your host data',
                        game_name, width,
                        height).run(game_name)
    # вот здесь надо от юзеров получать змейки и кидать в массив
    # По идее, надо просто передать змейку хосту и там уже всё запускать
    snakes = [Snake(name, width=width, height=height) for name in get_game(game_name)["snakes"]]
    for ind, snake in enumerate(snakes):
        body, direction = body_choice(ind, width, height)
        if body is not None and direction is not None:
            snake.body = body
            snake.head_pos = body[0]
            snake.direction = direction

    game = Game(snakes, width=width, height=height, speed=speed)
    update_game_var(game_name, "state", game.to_dict())
    update_game_var(game_name, "status", PLAYING)
    play(host=game_name,player_name= "HOST")


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
