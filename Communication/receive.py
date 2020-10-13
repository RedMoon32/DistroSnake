from redis import Redis
import json

r = Redis(host='localhost', port=12000)
FREE_GAMES = 'FREE_GAMES'


def get_key(key, client=r):
    res = client.get(key)
    if res:
        return json.loads(res)
    return None


def set_key(key, data, client=r):
    return client.set(key, json.dumps(data))


def create_game(name):
    games = get_key(FREE_GAMES)
    if not games:
        games = []
    games.append(f'{name}')
    set_key(FREE_GAMES, games)


def find_games():
    games = get_key(FREE_GAMES)
    if not games:
        return []
    return games


def start_game(name):
    games: list = get_key(FREE_GAMES)
    if name in games:
        games.remove(name)
        set_key(FREE_GAMES, games)
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
