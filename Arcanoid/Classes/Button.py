import pygame

from Arcanoid.utils import get_full_path


class Button:

    def __init__(self, left, top, width, height, default_image, hover_image, pressed_image, text=""):
        my_font = pygame.font.Font(get_full_path('Images', 'Capture_it.ttf'), 30)
        self.rect = pygame.Rect(left, top, width, height)
        self.left = left
        self.top = top
        self.default = default_image
        self.pressed = pressed_image
        self.hover = hover_image
        self.status = default_image
        self.text = my_font.render(text, False, (0, 0, 0))
        text_width, text_height = my_font.size(text)
        self.text_rect = pygame.Rect((left + (width - text_width) // 2, top + (height - text_height) // 2),
                                     (text_width, text_height))
