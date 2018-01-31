import pygame
from Arcanoid.utils import play_sound


class Bar:

    def __init__(self, length, height, x_screen, y_screen, image):
        self.length = length
        self._height = height
        self._x_screen = x_screen
        self._y_screen = y_screen
        self._top = y_screen - height
        self._left = (x_screen + length) // 2
        self._speed = 0
        self.basic_speed = 4
        self.rect = pygame.Rect((self._left, self._top), (self.length, self._height))
        self.old_rect = self.rect
        self.image = image

    def update(self):
        self.old_rect = self.rect
        self.rect = pygame.Rect((self._left, self._top), (self.length, self._height))

    def reset(self):
        self.image = "paddle104.png"
        self.length = 104
        self._speed = 0
        self.basic_speed = 4
        self._top = self._y_screen - self._height
        self._left = (self._x_screen + self.length) // 2
        self.update()

    def move(self, k_left, k_right):

        if k_right != k_left:

            if k_left:
                self._speed = min(self._speed, -self.basic_speed)
                self._left = max(0, self._left + self._speed)
                self._speed -= 0.2
            else:
                self._speed = max(self._speed, self.basic_speed)
                self._left = min(self._x_screen - self.length, self._left + self._speed)
                self._speed += 0.2

        else:
            self._speed = 0
        self.update()

    def bounce(self, ball):
        bounce_rect = self.rect.copy()
        bounce_rect.height = 1
        if bounce_rect.colliderect(ball.rect):
            ball.speed_x = ball.speed_x + self._speed / 4
            ball.speed_y = -ball.speed_y
            play_sound("jump.wav")
            return True
        return False
