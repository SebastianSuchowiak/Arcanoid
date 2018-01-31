import pygame
from Arcanoid.Classes.Ball import Ball
from Arcanoid.utils import play_sound


class Bonus:

    def __init__(self, top, left, y_screen, animation, animation_number, dead_animation="", dead_animation_num=0):
        self._speed = 1.5
        self.height = 30
        self.width = 30
        self._top = top
        self._left = left
        self.rect = pygame.Rect((self._left, self._top), (self.width, self.height))
        self.old_rect = None
        self.y_screen = y_screen
        self.animation_status = 0
        self.animation_image = animation
        self.animation_number = animation_number
        self.dead_animations = [dead_animation + str(x) + ".png" for x in range(1, dead_animation_num + 1)]

    def update(self):
        self.old_rect = self.rect
        self.rect = pygame.Rect((self._left, self._top), (self.width, self.height))

    def move(self):
        self._top += self._speed
        if self._top > self.y_screen:
            return False
        self.update()
        return True

    def give_animation(self):
        self.animation_status += 1
        self.animation_status %= 20 * self.animation_number
        return self.animation_image + str(self.animation_status // 20 + 1) + ".png"


def apply(bar, balls):
    pass


class SizeBonus(Bonus):

    def apply(self, bar, balls):
        if bar.length < 214:
            bar.length += 30
            bar.image = "paddle" + str(bar.length) + ".png"
            bar.update()
        play_sound("up.wav")


class Bomb(Bonus):

    def apply(self, bar, balls):
        if bar.length > 44:
            bar.length -= 30
            bar.image = "paddle" + str(bar.length) + ".png"
            bar.update()
        else:
            balls[0].hp -= 1
            balls[0].reset()
            bar.reset()
        play_sound("bomb.wav")


class BonusBall(Bonus):

    def apply(self, bar, balls):
        if len(balls) < 2:
            balls.append(Ball(800, 600, "ballBlue.png", 1))
        play_sound("bonus.wav")


class ExtraSpeed(Bonus):

    def apply(self, bar, balls):
        if balls[0].speed_y > 0:
            balls[0].speed_y += 1
        else:
            balls[0].speed_y -= 1
        play_sound("bonus.wav")
