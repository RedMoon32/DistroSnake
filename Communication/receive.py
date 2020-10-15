import itertools

from redis import Redis
import json

from Classes import consts
from Communication.communication_consts import FREE_GAMES, HOST, REDIS_FOUND, WAITING, NEW_GAME

i = -1
list_ = []


def get_redis_instances():
    return list_


def set_redis_instances(new_list):
    global list_
    list_ = new_list
    return


def flush_dbs():
    for db in list_:
        try:
            if len(db.client_list()) == 1:
                print("Flushed redis instance")
                db.flushdb()
        except:
            pass


client = None


def set_client(host, port):
    global client
    client = Redis(host=host, port=int(port))
    return client


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

        instances = []
        for player in players:
            alive_ = get_key(player)
            if not alive_:
                players.remove(player)
                set_key(game_name, res)
            else:
                instances.append(alive_)
        set_redis_instances(instances)
        if HOST in players:
            text = "Connected players: {}".format(",".join(players))
        else:
            text = "Host is off, please connect other room"

        game_text = font.render(text, True, consts.WHITE)
        screen.blit(
            game_text,
            (window.width / 2 - 200, window.height / 2),
        )


def get_key(key):
    global client
    try:
        res = client.get(key)
    except:
        repair_client()
        return get_key(key)

    if res:
        return json.loads(res)
    return None


def get_players_name(game_name):
    return get_game(game_name)["snakes"]


def repair_client():
    global client
    cur_cl = None
    global i
    while i < len(list_):
        i += 1
        cur_cl = Redis(list_[i][0], list_[i][1])
        try:
            if cur_cl.ping():
                break
        except:
            continue

    if i == len(list_):
        print(
            "All possible redis nodes checked, no working redis instance found, exiting the game"
        )
        import sys
        sys.exit(-1)
    else:
        print("Connected to other working redis - ", cur_cl)

    client = cur_cl
    if not get_key(REDIS_FOUND):
        set_key(REDIS_FOUND, True)
        set_key(WAITING, True, ex=2)
    while get_key(WAITING):
        pass


def set_key(key, data, **kwargs):
    global client
    try:
        return client.set(key, json.dumps(data), **kwargs)
    except:
        print("Failed, trying again with diff redis")
        repair_client()
        return set_key(key, data, **kwargs)


def create_game(name):
    games = get_key(FREE_GAMES)
    new_game = NEW_GAME.copy()
    new_game["snakes"].append(HOST)
    set_key(name, new_game)
    if not games:
        games = []
    games.append(f"{name}")
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

    if games is not None and game_name in games:
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
