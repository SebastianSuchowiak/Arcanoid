import os
import pygame
import json
from datetime import datetime

from Arcanoid.Functions import game

ROOT_DIR = os.path.dirname(__file__)


def get_full_path(*path):
    return os.path.join(ROOT_DIR, *path)


def get_image(filename: str):
    image = game.image_library.get(filename)
    if image is None:
        path = get_full_path('Images', filename)
        image = pygame.image.load_extended(path)
        game.image_library[filename] = image
    return image


def play_sound(filename: str):
    sound = game.sound_library.get(filename)
    if sound is None:
        path = get_full_path('Sounds', filename)
        sound = pygame.mixer.Sound(path)
        game.sound_library[filename] = sound
    sound.play()


def add_to_rank(timer, level):
    with open(get_full_path('config.json'), "r") as fin:
        config = json.load(fin)
        ranking = config["high_scores"][level]
        times = list(ranking.values())
        times.append(timer)
        sortfunc = lambda t: datetime.strptime(t, '%M:%S')
        times.sort(key=lambda t: sortfunc(t))
        config["high_scores"][level] = dict(zip(range(1, 6), times))

        with open(get_full_path('config.json'), "w") as fout:
            json.dump(config, fout, indent=4)


def get_rank(level):
    with open(get_full_path('config.json'), "r") as fin:
        config = json.load(fin)
        ranking = config["high_scores"][level]
        rank_list = []
        for i in range(1, len(ranking) + 1):
            rank_list.append("#" + str(i) + ". " + ranking[str(i)])
        return rank_list
