import pygame

from Arcanoid.Classes.Button import Button
from Arcanoid.utils import get_image, play_sound


def intro_loop(screen):

    width = 800
    height = 600
    clock = pygame.time.Clock()
    not_done = True

    b_start = Button(100, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "STANDARD")
    b_exit = Button(510, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "EXIT")
    b_levels = Button(305, 300, 190, 71, "standard.png", "hover.png", "clicked.png", "LEVELS")
    screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), (0, 0))
    screen.blit(pygame.transform.scale(get_image("Arkanoid.png"), (800, 300)), (0, 0))

    buttons = [b_start, b_exit, b_levels]

    while not_done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, "0"

        if b_start.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            play_sound("click.wav")
            return 3, "0"
        elif b_exit.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            play_sound("click.wav")
            return 0, "0"
        elif b_levels.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            play_sound("click.wav")
            return 2, "0"

        mouse = pygame.mouse.get_pos()
        for button in buttons:
            if button.rect.collidepoint(mouse):
                button.status = button.hover
                if pygame.mouse.get_pressed()[0]:
                    button.status = button.pressed
            else:
                button.status = button.default

        clock.tick(30)
        for button in buttons:
            screen.blit(get_image(button.status), button.rect)
            screen.blit(button.text, button.text_rect)
        pygame.display.update()
