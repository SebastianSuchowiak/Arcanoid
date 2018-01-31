import pygame
from time import time
from Arcanoid.utils import play_sound


class Ball:

    def __init__(self, x_screen, y_screen, image, hp=3):
        self._height = 22
        self._width = 22
        self._x_screen = x_screen
        self._y_screen = y_screen
        self.top = y_screen / 2
        self.left = (x_screen + self._width) / 2
        self.speed_x = 0
        self.speed_y = 2
        self.rect = pygame.Rect((self.left, self.top), (self._width, self._height))
        self.dirty_rect = self.rect
        self.hp = hp
        self.clock = time()
        self.image = image

    def update(self):
        self.dirty_rect = self.rect
        self.rect = pygame.Rect((self.left, self.top), (self._width, self._height))

    def reset(self):
        self.top = self._y_screen / 2 * 1
        self.left = (self._x_screen + self._width) / 2
        self.speed_x = 0
        self.speed_y = 2
        self.rect = pygame.Rect((self.left, self.top), (self._width, self._height))

    def move(self):

        if self.top + self.speed_y - self._height / 2 > self._y_screen:
            self.hp -= 1
            if self.hp < 0:
                return True
            return False

        elif self.top + self.speed_y < 0:
            play_sound("jump.wav")
            self.speed_y = -self.speed_y
        elif 0 > self.left or self.left + self._width > self._x_screen:
            play_sound("jump.wav")
            self.speed_x = -self.speed_x

        self.top += self.speed_y
        self.left += self.speed_x
        self.update()

        return True

    def break_block(self, block):
        if self.rect.colliderect(block.rect):
            block.toughness -= 1
            self.speed_x *= 3/4
            if time() - self.clock > 1:
                self.clock = time()
                self.speed_y = -self.speed_y
            if block.toughness == 0:
                self.speed_x += block.bonus_speed
            return True
        return False
