import pygame
from redis import Redis
import json

from Classes import consts

r = Redis(host='localhost', port=6379)
# r = Redis(host='10.91.89.94', port=6379)
FREE_GAMES = 'FREE_GAMES'
HOST = "HOST"

PLAYING = "PLAYING"
PENDING = "PENDING"

NEW_GAME = {"snakes": [], "master": HOST, "status": "PENDING", "state": None}

i = 0


def update_game_var(game_name, game_var, new_val):
    game = get_game(game_name)
    game[game_var] = new_val
    set_key(game_name, game)


def render_players(game_name, font, window, screen):
    if game_name:
        res = get_game(game_name)
        if not res:
            return
        players = res["snakes"]

        for player in players:
            if not get_key(player):
                players.remove(player)
                set_key(game_name, res)
        if HOST in players:
            text = 'Connected players: {}'.format(','.join(players))
        else:
            text = 'Host is off, please connect other room'

        game_text = font.render(text, True, consts.WHITE)
        screen.blit(game_text, (window.width / 2 - 200, window.height / 2), )


def get_key(key, client=r):
    res = client.get(key)
    if res:
        return json.loads(res)
    return None


def get_players_name(game_name):
    return get_game(game_name)["snakes"]


def set_key(key, data, client=r, **kwargs):
    return client.set(key, json.dumps(data), **kwargs)


def create_game(name):
    games = get_key(FREE_GAMES)
    new_game = NEW_GAME.copy()
    new_game["snakes"].append(HOST)
    set_key(name, new_game)
    if not games:
        games = []
    games.append(f'{name}')
    set_key(FREE_GAMES, games)


def get_game(game_name):
    return get_key(game_name)


def find_games():
    games = get_key(FREE_GAMES)
    if not games:
        return []
    return games


def start_game(game_name):
    games: list = get_key(FREE_GAMES)
    if game_name in games:
        games.remove(game_name)
        set_key(FREE_GAMES, games)
        return True
    else:
        return False


def connect_to_game(game_name, player_name):
    games = get_key(FREE_GAMES)
    if game_name in games:
        game = get_key(game_name)
        game["snakes"].append(player_name)
        set_key(game_name, game)


def make_move():
    pass


def get_state():
    pass


def update_state():
    pass
