import pygame
from Arcanoid.Classes.Button import Button
from Arcanoid.utils import get_image, play_sound


def level_loop(screen):
    width = 800
    height = 600
    clock = pygame.time.Clock()

    not_done = True

    level_buttons = []
    button_num = 1
    for y in range(73, height - 253, 91):
        for x in range(82, width - 82, 91):
            level_buttons.append(Button(x, y, 71, 71,
                                        "standardoval.png", "hoveroval.png", "clickedoval.png", str(button_num)))
            button_num += 1
    del button_num

    level_buttons.insert(0, Button(305, 450, 190, 71, "standard.png", "hover.png", "clicked.png", "BACK"))
    screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), (0, 0))

    while not_done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, "0"

        if level_buttons[0].status == "clicked.png" and not pygame.mouse.get_pressed()[0]:
            play_sound("click.wav")
            return 1, "0"

        for i, button in enumerate(level_buttons[1:]):
            if button.status == "clickedoval.png" and not pygame.mouse.get_pressed()[0]:
                play_sound("click.wav")
                if i <= 4:
                    return 3, str(i + 1)

        mouse = pygame.mouse.get_pos()
        for button in level_buttons:
            if button.rect.collidepoint(mouse):
                button.status = button.hover
                if pygame.mouse.get_pressed()[0]:
                    button.status = button.pressed
            else:
                button.status = button.default

        for button in level_buttons:
            screen.blit(get_image(button.status), button.rect)
            screen.blit(button.text, button.text_rect)

        pygame.display.update()
        clock.tick(30)
