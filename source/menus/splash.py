import pygame
import time
import sys

from source import main
from source.menus import main_menu
from source.shaders.CA import Abber

def run(screen, assets, clock, draw_fps):
    pygame.display.set_caption("Strike Four")
    clock = main.clock

    splash_img = assets["images/splash.png"]
    splash_sound = assets["sfx/rizz.wav"]

    splash_sound.play()

    start_time = time.time()

    chroma = Abber(offset=2)

    w, h = screen.get_size()
    scene_surface = pygame.Surface((w, h))

    running = True
    while running:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))

        rect = splash_img.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        scene_surface.blit(splash_img, rect)

        chroma.apply(screen, scene_surface)

        draw_fps(screen, clock)
        clock.tick(main.fps)

        pygame.display.flip()

        if time.time() - start_time >= 1.5:
            running = False

    main_menu.run(screen, assets, clock, draw_fps)

