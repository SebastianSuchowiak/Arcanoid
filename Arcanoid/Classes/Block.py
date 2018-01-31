import pygame
from random import randint
from Arcanoid.Classes.Bonus import Bonus, Bomb, BonusBall, ExtraSpeed
from Arcanoid.Classes.Bonus import SizeBonus


class Block:

    def __init__(self, top, left, width, height, bonus_type, toughness=1):
        self.rect = pygame.Rect(left, top, width, height)

        self.toughness = toughness
        self.bonus_speed = 0
        self.bonus = Bonus
        self.bonused = True
        self.bonus_type = bonus_type
        self.image = "purple.png"
        if self.bonus_type == -1:
            self.bonus_type = randint(1, 10)
        self.get_bonus()
        self.bonus_speed = randint(-1, 1)

    def get_bonus(self):
        bonus_top = self.rect.top + self.rect.height - 15
        bonus_left = self.rect.left + self.rect.width // 2 - 15
        if self.bonus_type == 1:
            self.bonus = SizeBonus(bonus_top, bonus_left,
                                   600, "orb", 10, "orbboom", 6)
            self.image = "blue.png"
        elif self.bonus_type == 2:
            self.bonus = Bomb(bonus_top, bonus_left,
                              600, "bomb", 5, "boom", 11)
            self.image = "red.png"
        elif self.bonus_type == 3:
            self.bonus = BonusBall(bonus_top, bonus_left,
                                   600, "planet", 8, "greenboom", 6)
            self.image = "yellow.png"
        elif self.bonus_type == 4:
            self.bonus = ExtraSpeed(bonus_top, bonus_left,
                                    600, "redbubble", 7, "redbubbleboom", 6)
            self.image = "green.png"
        else:
            self.bonused = False
