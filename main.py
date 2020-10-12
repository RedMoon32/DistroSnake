import sys

import pygame

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Game import Game
from Classes.Snake import Snake
from Classes.HostOrPlayerScreen import HostOrPlayerScreen
from Classes.WaitScreen import WaitSreen
from Classes.HostScreen import HostScreen
from Classes import consts


def run(width=consts.WIDTH, height=consts.HEIGHT, speed=consts.SPEED):
    while True:
        # returns True if player else False . If something goes wrong - None
        hostOrGamer = HostOrPlayerScreen(width=width, height=height).run()

        if hostOrGamer is not None:
            if hostOrGamer:
                close, host = DataEnteringScreen('Initialization window', 'Enter host', width, height).run()
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
            else:
                # Хост используется как имя для змеи, там вылезает баг при попытке ввести имя
                # Я не хочу разбираться, извините
                host = "HOOOOOOOOST"
                res, _ = HostScreen('Your host data',
                                                   'Your host is <сюда хост и прочее> {}'.format(host), width,
                                                   height).run()
                if res:
                    # host = DataEnteringScreen('What is your name?', 'Enter name', 720, 460).run()
                    # if host is not None:
                    # вот здесь надо от юзеров получать змейки и кидать в массив
                    snakes = [Snake(host, width=width, height=height), Snake("test", width=width, height=height)]

                    Game(snakes, width=width, height=height).run()
                else:
                    sys.exit()
        else:
            break


run()
