from Classes.NameEntering import NameEntering
from Classes.Game import Game
from Classes.Snake import Snake

name = NameEntering(width=720, height=460).run()
snakes = [Snake(name, width=720, height=460)][0]
game = Game(snakes, width=720, height=460)
game.run()
