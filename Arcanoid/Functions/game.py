import pygame

from Arcanoid.Functions.game_loop import game_loop
from Arcanoid.Functions.intro_loop import intro_loop
from Arcanoid.Functions.level_loop import level_loop
from Arcanoid.utils import get_image, get_full_path

image_library = {}
sound_library = {}


def main_loop():
    status = 1
    pygame.mixer.pre_init(44100, -16, 1, 512)
    pygame.init()
    pygame.font.init()
    pygame.mixer.music.load(get_full_path("Sounds", "golce1.wav"))
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Arcanoid")
    pygame.display.set_icon(get_image("icon.png"))
    level = "0"
    pygame.mixer.music.play(-1)
    while status != 0:
        if status == 1:
            status, level = intro_loop(screen)
        elif status == 2:
            status, level = level_loop(screen)
        elif status == 3:
            pygame.mixer.music.stop()
            status, level = game_loop(screen, level)
            pygame.mixer.music.play(-1)
    pygame.quit()
