import pygame

from Arcanoid.Classes.Button import Button
from Arcanoid.utils import get_image, get_full_path, get_rank, play_sound


def win_loop(screen, level):
    width = 800
    clock = pygame.time.Clock()
    not_done = True
    my_font = pygame.font.Font(get_full_path('Images', 'Capture_it.ttf'), 140)
    rank_font = pygame.font.Font(get_full_path('Images', 'Capture_it.ttf'), 40)

    b_reset = Button(100, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "RESET")
    b_menu = Button(510, 400, 190, 71, "standard.png", "hover.png", "clicked.png", "MENU")
    win_text = my_font.render("You Won!", False, (255, 255, 255))
    text_width, text_height = my_font.size("You Won!")
    screen.blit(win_text, ((width - text_width) // 3, 50))
    text_width, text_height = rank_font.size("5#. 59:59")
    for i, place in enumerate(get_rank(level)):
        text = rank_font.render(place, False, (255, 255, 255))
        screen.blit(text, ((width - text_width) // 2, 200 + i * text_height))

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
