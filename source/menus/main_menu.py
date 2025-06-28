import pygame
import sys
import math
from source import main
from source.logic.s4_game_logic import run_connect_four
from source.main import scroll_state, fade_speed, difficulty
from source.shaders.CA import Abber
from source.utils import AnimatedButton, SpriteSheetAtlas, SM, size, lerp
from source.menus import options

def run(screen, assets, clock, draw_fps):
    pygame.display.set_caption("Strike Four | Main Menu")
    clock = main.clock

    logo_img = size(assets["images/ui/menu/logo.png"], 0.7)
    chooseDif = size(assets["images/ui/menu/choose.png"], 0.8)

    split = size(assets["images/split.png"], 1).convert_alpha()
    split_alpha = 0
    split_fading_in = False
    split_visible = False

    dither = assets["images/dither.png"]
    grid_img = assets["images/grid.png"]

    menu_music = SM(assets["music/menu_temp.wav"], "music")
    menu_music.set_volume(main.volumes["music"])
    menu_music.play(loops=-1)

    buttons = []

    play_btn = AnimatedButton(
        SpriteSheetAtlas(
            assets["images/ui/menu/Play.png"],
            assets["images/ui/menu/Play.xml"]
        ),
        name="play",
        pos=(325, 250)
    )
    play_btn.add_animation("normal", "normal_play")
    play_btn.add_animation("hover", "hover_play")
    buttons.append(play_btn)

    options_btn = AnimatedButton(
        SpriteSheetAtlas(
            assets["images/ui/menu/Options.png"],
            assets["images/ui/menu/Options.xml"]
        ),
        name="options",
        pos=(255, 350)
    )
    options_btn.add_animation("normal", "normal_options")
    options_btn.add_animation("hover", "hover_options")
    buttons.append(options_btn)

    quit_btn = AnimatedButton(
        SpriteSheetAtlas(
            assets["images/ui/menu/Quit.png"],
            assets["images/ui/menu/Quit.xml"]
        ),
        name="quit",
        pos=(325, 450)
    )
    quit_btn.add_animation("normal", "normal_quit")
    quit_btn.add_animation("hover", "hover_quit")
    buttons.append(quit_btn)

    difficulty_buttons = []

    easy_btn = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/difficulties/easy.png"], assets["images/ui/difficulties/easy.xml"]),
        name="easy",
        pos=(1000, 250)
    )
    easy_btn.add_animation("normal", "easy idle")
    easy_btn.add_animation("hover", "easy hover")
    difficulty_buttons.append(easy_btn)

    medium_btn = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/difficulties/medium.png"], assets["images/ui/difficulties/medium.xml"]),
        name="medium",
        pos=(1000, 350)
    )
    medium_btn.add_animation("normal", "medium idle")
    medium_btn.add_animation("hover", "medium hover")
    difficulty_buttons.append(medium_btn)

    hard_btn = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/difficulties/hard.png"], assets["images/ui/difficulties/hard.xml"]),
        name="hard",
        pos=(1000, 450)
    )
    hard_btn.add_animation("normal", "hard idle")
    hard_btn.add_animation("hover", "hard hover")
    difficulty_buttons.append(hard_btn)

    #for animating purposes
    #theres probably a better way to do this but god dayum im not gonna sit and figure it out
    logo_pos = [400, 125]
    chooseDif_pos = [1000, 265]
    play_btn.pos = [325, 250]
    options_btn.pos = [255, 350]
    quit_btn.pos = [325, 450]

    logo_target_x = 175
    chooseDif_target_x = 450
    play_target_x = 50
    options_target_x = 50
    quit_target_x = 50

    easy_btn.pos = [1000, 250]
    medium_btn.pos = [1000, 350]
    hard_btn.pos = [1000, 450]

    easy_target_x = 600
    medium_target_x = 500
    hard_target_x = 585

    tile_size = 128

    offset_x = scroll_state["offset_x"]
    offset_y = scroll_state["offset_y"]

    scroll_x = scroll_state["scroll_x"]
    scroll_y = scroll_state["scroll_y"]

    scroll_state["offset_x"] = offset_x
    scroll_state["offset_y"] = offset_y

    flash_duration = 750
    flash_start_time = pygame.time.get_ticks()

    w, h = screen.get_size()

    chroma = Abber(offset=main.shaderVal)

    # this is off-screen, we just draw on it and show to screen
    scene_surface = pygame.Surface((w, h))

    font = pygame.font.Font("../assets/fonts/undertalesans.ttf", 18)

    show_difficulties = False
    is_moving = False
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # really shitty fix since python doesn't have switch case statements
            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                mouse_pos = e.pos
                for btn in buttons:
                    if btn.get_rect().collidepoint(mouse_pos):
                        if btn.name == "quit":
                            pygame.quit()
                            sys.exit()
                        elif btn.name == "play":
                            is_moving = True
                            show_difficulties = True
                            split_fading_in = True
                        elif btn.name == "options":
                            volumes, fullscreen, shader = options.settings_menu(screen,
                                                                                assets,
                                                                                main.volumes,
                                                                                main.fullscreen,
                                                                                main.shader,
                                                                                clock,
                                                                                menu_music,
                                                                                draw_fps)
                            main.volumes = volumes
                            main.fullscreen = fullscreen
                            main.shader = shader
                            menu_music.set_volume(volumes["music"])
                            logo_pos = [400, 125] # this is shit, never do this, but im on a time limit and i dont care
                            chooseDif_pos = [1000, 265]
                            play_btn.pos = [325, 250]
                            options_btn.pos = [255, 350]
                            quit_btn.pos = [325, 450]

                            easy_btn.pos = [1000, 250]
                            medium_btn.pos = [1000, 350]
                            hard_btn.pos = [1000, 450]
                            split_alpha = 0

                            is_moving = False
                            split_visible = False
                            show_difficulties = False

                for btn in difficulty_buttons:
                    if btn.get_rect().collidepoint(mouse_pos):
                        if btn.name == "easy":
                            main.difficulty = "easy"
                            menu_music.stop()
                            run_connect_four(screen, assets, main.difficulty, draw_fps)
                        elif btn.name == "medium":
                            main.difficulty = "medium"
                            menu_music.stop()
                            run_connect_four(screen, assets, main.difficulty, draw_fps)
                        elif btn.name == "hard":
                            main.difficulty = "hard"
                            menu_music.stop()
                            run_connect_four(screen, assets, main.difficulty, draw_fps)

        offset_x += scroll_x
        offset_y += scroll_y

        if offset_x <= -tile_size:
            offset_x += tile_size
        elif offset_x >= tile_size:
            offset_x -= tile_size

        if offset_y <= -tile_size:
            offset_y += tile_size
        elif offset_y >= tile_size:
            offset_y -= tile_size

        scroll_state["offset_x"] = offset_x
        scroll_state["offset_y"] = offset_y

        scene_surface.fill((0, 0, 0))
        cols = w // tile_size + 8
        rows = h // tile_size + 8

        for row in range(rows):
            for col in range(cols):
                x = col * tile_size + offset_x
                y = row * tile_size + offset_y
                scene_surface.blit(grid_img, (x, y))

        scene_surface.blit(dither,(0,0))
        time_elapsed = pygame.time.get_ticks() / 750
        float_offset = math.sin(time_elapsed * 2 * math.pi / 3) * 10

        #draw images here

        rect = logo_img.get_rect(center=(int(logo_pos[0]), int(logo_pos[1] + float_offset)))
        scene_surface.blit(logo_img, rect)

        rect = chooseDif.get_rect(center=(int(chooseDif_pos[0]), int(chooseDif_pos[1] + float_offset)))
        scene_surface.blit(chooseDif, rect)

        dt = clock.tick(main.fps)
        mouse_pos = pygame.mouse.get_pos()

        if is_moving:
            logo_pos[0] = lerp(logo_pos[0], logo_target_x, 0.1)
            chooseDif_pos[0] = lerp(chooseDif_pos[0], chooseDif_target_x, 0.1)

            play_btn.pos[0] = lerp(play_btn.pos[0], play_target_x, 0.1)
            options_btn.pos[0] = lerp(options_btn.pos[0], options_target_x, 0.1)
            quit_btn.pos[0] = lerp(quit_btn.pos[0], quit_target_x, 0.1)

            if (abs(logo_pos[0] - logo_target_x) < 1 and
                    abs(chooseDif_pos[0] - chooseDif_target_x) < 1 and
                    abs(play_btn.pos[0] - play_target_x) < 1 and
                    abs(options_btn.pos[0] - options_target_x) < 1 and
                    abs(quit_btn.pos[0] - quit_target_x) < 1):
                is_moving = False

                logo_pos[0] = logo_target_x
                chooseDif_pos[0] = chooseDif_target_x
                play_btn.pos[0] = play_target_x
                options_btn.pos[0] = options_target_x
                quit_btn.pos[0] = quit_target_x

        if show_difficulties:
            easy_btn.pos[0] = lerp(easy_btn.pos[0], easy_target_x, 0.1)
            medium_btn.pos[0] = lerp(medium_btn.pos[0], medium_target_x, 0.1)
            hard_btn.pos[0] = lerp(hard_btn.pos[0], hard_target_x, 0.1)\

        if split_fading_in: # this is so hacky and stupid, but i dont have enough time to make a util for it
            split_alpha += fade_speed * (dt / 350)
            if split_alpha >= 255:
                split_alpha = 255
                split_fading_in = False
                split_visible = True
            split.set_alpha(int(split_alpha))
        elif split_visible:
            split.set_alpha(255)
        else:
            split.set_alpha(0)

        for btn in buttons:
            btn.update(dt, mouse_pos)
            btn.draw(scene_surface)

        for btn in difficulty_buttons:
            btn.update(dt, mouse_pos)
            btn.draw(scene_surface)

        version_text = font.render(f"v1.0.0", True, (34, 32, 32))
        scene_surface.blit(version_text, (25, 575))

        split_rect = split.get_rect()
        scene_surface.blit(split, split_rect)

        #dont go past this or else shit gets drawn above the flash

        #flash for extra cool points lol
        time_since_flash = pygame.time.get_ticks() - flash_start_time
        if time_since_flash < flash_duration:
            alpha = 255 - int((time_since_flash / flash_duration) * 255)
            flash_overlay = pygame.Surface((w, h)).convert_alpha()
            flash_overlay.fill((255, 255, 255, alpha))
            scene_surface.blit(flash_overlay, (0, 0))

        # NEVER EVER FUCKING TOUCH THIS, DONT CHANGE IT, DONT REMOVE IT, LEAVE IT BE
        if main.shader:
            chroma.apply(screen, scene_surface)
        else:
            screen.blit(scene_surface, (0, 0))

        draw_fps(screen, clock)

        pygame.display.flip()