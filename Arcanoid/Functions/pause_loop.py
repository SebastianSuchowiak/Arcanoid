import pygame
from Arcanoid.Classes.Button import Button
from Arcanoid.utils import get_image, play_sound


def pause_loop(screen_image):
    pygame.init()
    width = 800
    height = 600
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    not_done = True
    screen.blit(screen_image, (0, 0))
    screen.blit(get_image("pause.png"), (width // 2 - 125, height // 2 - 115))

    b_reset = Button(100, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "RESET")
    b_menu = Button(510, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "MENU")

    buttons = [b_menu, b_reset]

    while not_done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

        if b_reset.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            screen.blit(screen_image, (0, 0))
            play_sound("click.wav")
            pygame.display.update()
            return 3
        elif b_menu.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            screen.blit(screen_image, (0, 0))
            pygame.display.update()
            play_sound("click.wav")
            return 1

        mouse = pygame.mouse.get_pos()
        for button in buttons:
            if button.rect.collidepoint(mouse):
                button.status = button.hover
                if pygame.mouse.get_pressed()[0]:
                    button.status = button.pressed
            else:
                button.status = button.default

        clock.tick(60)
        for button in buttons:
            screen.blit(get_image(button.status), button.rect)
            screen.blit(button.text, button.text_rect)
        pygame.display.update()

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            while pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.event.get()
            not_done = False
            screen.blit(screen_image, (0, 0))

    return -1
