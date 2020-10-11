import pygame

from Classes.DataEnteringScreen import DataEnteringScreen
from Classes.Game import Game
from Classes.Snake import Snake
from Classes.HostOrPlayerScreen import HostOrPlayerScreen
from Classes.WaitScreen import WaitSreen


# returns (True, None) if player else (False, None) . If something goes wrong - None, None
hostOrGamer = HostOrPlayerScreen(width=720, height=460).run()

if hostOrGamer is not None:

    if hostOrGamer:
        host = DataEnteringScreen('Initialization window', 'Enter host', 720, 460).run()
        #  по хосту подключаться, используй как хочешь
        name = DataEnteringScreen('What is your name?', 'Enter name', 720, 460).run()
        snakes = [Snake(name, width=720, height=460), Snake("test", width=720, height=460)]
        success = WaitSreen().run()
        game = Game(snakes, width=720, height=460).run()
    else:
        #TODO сделать окно для вывода IP и старта игры
        host_data = DataEnteringScreen('Host data', 'Your ip is <сюда вставь короче>', 720, 460).run()
        name = DataEnteringScreen('What is your name?', 'Enter name', 720, 460).run()
        snakes = [Snake(name, width=720, height=460)]
        game = Game(snakes, width=720, height=460).run()

