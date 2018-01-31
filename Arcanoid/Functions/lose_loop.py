import pygame

from Arcanoid.Classes.Button import Button
from Arcanoid.utils import get_image, get_full_path, play_sound


def lose_loop(screen):
    width = 800
    height = 600
    clock = pygame.time.Clock()
    not_done = True
    my_font = pygame.font.Font(get_full_path('Images', 'Capture_it.ttf'), 140)

    b_reset = Button(100, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "RESET")
    b_menu = Button(510, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "MENU")
    lost_text = my_font.render("You Lose!", False, (255, 255, 255))
    text_width, text_height = my_font.size("You Lose!")
    screen.blit(lost_text, ((width - text_width) // 2, (height - text_height) // 2))

    buttons = [b_menu, b_reset]

    while not_done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0

        if b_reset.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            play_sound("click.wav")
            return 3
        elif b_menu.status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
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

        clock.tick(30)
        for button in buttons:
            screen.blit(get_image(button.status), button.rect)
            screen.blit(button.text, button.text_rect)
        pygame.display.update()
