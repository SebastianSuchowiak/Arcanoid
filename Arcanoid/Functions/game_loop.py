import pygame

from Arcanoid.Classes.Animation import Animation
from Arcanoid.Classes.Ball import Ball
from Arcanoid.Classes.Bar import Bar
from Arcanoid.Classes.Block import Block
from Arcanoid.Functions.pause_loop import pause_loop
from Arcanoid.Functions.lose_loop import lose_loop
from Arcanoid.Functions.win_loop import win_loop
from Arcanoid.utils import get_image, get_full_path, add_to_rank, play_sound


def get_lvl_blocks(level):
    with open(get_full_path('Levels', level), "r") as f:
        raw_text = f.read()
        blocks_attributes = [list(map(int, x.split()))for x in raw_text.split("\n") if x]
        blocks = [Block(x[0], x[1], x[2], x[3], x[4]) for x in blocks_attributes]
        return blocks


FPS = 120


def game_loop(screen, level="0"):
    myfont = pygame.font.Font(get_full_path('Images', 'Capture_it.ttf'), 30)
    width = 800
    height = 600
    clock = pygame.time.Clock()
    screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), (0, 0))
    not_done = True
    dirty_rects = []
    pause_time = 0
    old_secs = -1
    start = pygame.time.get_ticks()
    time_rect = pygame.Rect((20, 10), (30 * 3, 30))

    bar = Bar(104, 24, width, height, "paddle104.png")
    hp = 3
    start_ball = Ball(width, height, "ballGrey.png", hp)
    blocks = []
    bonuses = []
    animations = []
    balls = [start_ball]
    block_num = 0
    timer = "00:00"
    block_w = 70
    block_h = 35
    bounce_timers = []

    if level == "0":
        for x in range(0, width, block_w):
            for y in range(50, height // 3, block_h):
                blocks.append(Block(y, x, block_w, block_h, -1))
                block_num += 1
    else:
        blocks = get_lvl_blocks(level)
        block_num = len(blocks)

    max_top = 0
    for block in blocks:
        screen.blit(pygame.transform.scale(get_image(block.image), (block.rect.width, block.rect.height)),
                    (block.rect.left, block.rect.top))
        if block.rect.top > max_top:
            max_top = block.rect.top

    blocks_rect = pygame.Rect((0, 0), (width, max_top + 60))
    del max_top
    life_rects = [pygame.Rect((width - (40 + i * 40), 10), (40, 40)) for i in range(start_ball.hp, 0, -1)]

    while not_done:

        if block_num == 0:
            add_to_rank(timer, level)
            play_sound("tuturu.wav")
            return win_loop(screen, level), level

        hp = balls[0].hp
        for i, ball in enumerate(balls):
            if not ball.move() and i == 0:
                ball.reset()
                dirty_rects.append(bar.rect)
                bar.length = 104
                bar.image = "paddle" + str(bar.length) + ".png"
                bar.update()
            dirty_rects.append(ball.dirty_rect)
            if ball.hp == 0:
                del balls[i]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0, level

        if len(life_rects) != hp:
            dirty_rects.append(life_rects[0])
            del life_rects[0]

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_SPACE]:
            while pygame.key.get_pressed()[pygame.K_SPACE]:
                pygame.event.get()
            before = pygame.time.get_ticks()
            status = pause_loop(screen.copy())
            if status == 0:
                pygame.quit()
                return 0, level
            elif status == 1:
                return 1, level
            elif status == 3:
                return 3, level
            pause_time += (pygame.time.get_ticks() - before)

        if len(bounce_timers) < len(balls):
            bounce_timers.append(0)
        for i in range(len(balls)):
            if pygame.time.get_ticks() - bounce_timers[i] > 500:
                if bar.bounce(balls[i]):
                    bounce_timers[i] = pygame.time.get_ticks()

        bar.move(pressed[pygame.K_LEFT], pressed[pygame.K_RIGHT])
        dirty_rects.append(bar.old_rect)

        for ball in balls:
            if blocks_rect.contains(ball.rect):
                for i, block in enumerate(blocks):
                    screen.blit(pygame.transform.scale(get_image(block.image), (block.rect.width, block.rect.height)),
                                (block.rect.left, block.rect.top))
                    if ball.break_block(block):
                        if block.toughness == 0:
                            play_sound("break.wav")
                            if block.bonused:
                                bonuses.append(block.bonus)
                            dirty_rects.append(block.rect)
                            block_num -= 1
                            del blocks[i]

        for i, bonus in enumerate(bonuses):
            if bonus.move():
                dirty_rects.append(bonus.old_rect)
                if bar.rect.colliderect(bonus.rect):
                    bonus.apply(bar, balls)
                    if len(bonus.dead_animations) > 0:
                        animations.append(Animation(bonus.dead_animations, bonus.rect))
                    del bonuses[i]
            else:
                dirty_rects.append(bonus.old_rect)
                del bonuses[i]

        for rect in dirty_rects:
            screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), rect, rect)
        dirty_rects = []

        for bonus in bonuses:
            screen.blit(pygame.transform.scale(get_image(bonus.give_animation()), (bonus.width, bonus.height)),
                        (bonus.rect.left, bonus.rect.top))

        for i, animation in enumerate(animations):
            image = animation.get_current()
            rect = animation.rect
            if len(image) > 0:
                screen.blit(pygame.transform.scale(get_image(image), (rect.width, rect.height)),
                            (rect.left, rect.top))
                dirty_rects.append(rect)
            else:
                del animations[i]

        screen.blit(get_image(bar.image), (bar.rect.left, bar.rect.top))
        for ball in balls:
            screen.blit(get_image(ball.image), (ball.left, ball.top))

        secs = (pygame.time.get_ticks() - pause_time - start) // 1000
        if secs != old_secs:
            old_secs = secs
            mins = secs // 60
            secs = secs % 60
            if len(str(secs)) > 1:
                timer = "0" + str(mins) + ":" + str(secs)
            else:
                timer = "0" + str(mins) + ":" + "0" + str(secs)
            screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), time_rect, time_rect)
            screen.blit(myfont.render(timer, False, (255, 255, 255)), time_rect)

        for life in life_rects:
            screen.blit(get_image("heart.png"), life)

        pygame.display.update()
        clock.tick(FPS)

        if not bool(start_ball.hp):
            rect = life_rects[0]
            screen.blit(pygame.transform.scale(get_image("background.png"), (width, height)), rect, rect)
            play_sound("lose.wav")
            return lose_loop(screen), level
