from redis import Redis
import json
import random

r = Redis(host='localhost', port=12000)
FREE_GAMES = 'FREE_GAMES'


def get_key(key, client=r):
    return json.loads(client.get(key))


def set_key(key, data, client=r):
    return client.set(key, json.dumps(data))


def create_game(name):
    games = get_key(FREE_GAMES)
    if not games:
        games = []
    games.append(f'New Game #{name}')


def find_game():
    games = get_key(FREE_GAMES)
    return games


def start_game(name):
    games: list = get_key(FREE_GAMES)
    if name in games:
        games.remove(name)
        return True
    else:
        return False


def connect_to_game(name):
    games = get_key(FREE_GAMES)
    if name in games:
        pass


def make_move():
    pass


def get_state():
    pass


def update_state():
    pass
