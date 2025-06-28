import math

import pygame
import sys

from source import main
from source.main import scroll_state
from source.shaders.CA import Abber
from source.utils import AnimatedButton, SpriteSheetAtlas
from source.utils import size
from source.utils import DragDebugger

def settings_menu(screen, assets, volumes, fullscreen, shader, clock, menu_music, draw_fps):
    pygame.display.set_caption("Strike Four | Settings")

    w, h = screen.get_size()

    drag_debugger = DragDebugger()

    font = pygame.font.Font("../assets/fonts/undertalesans.ttf", 30)
    chroma = Abber(offset=main.shaderVal)

    tile_size = 128

    offset_x = scroll_state["offset_x"]
    offset_y = scroll_state["offset_y"]

    scroll_x = scroll_state["scroll_x"]
    scroll_y = scroll_state["scroll_y"]

    scroll_state["offset_x"] = offset_x
    scroll_state["offset_y"] = offset_y

    logo_img = size(assets["images/ui/menu/logo.png"], 0.7)
    grid_img = assets["images/grid.png"]

    # lord forgive me for this sin.
    # but there was no other way for me to cleanly do this
    music_minus = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/menu/Minus.png"], assets["images/ui/menu/Minus.xml"]),
        name="music_minus", pos=(310, 280))
    music_minus.add_animation("normal", "minus_normal")
    music_minus.add_animation("hover", "minus_hover")

    music_plus = AnimatedButton(SpriteSheetAtlas(assets["images/ui/menu/Plus.png"], assets["images/ui/menu/Plus.xml"]),
                                name="music_plus", pos=(470, 280))
    music_plus.add_animation("normal", "plus_normal")
    music_plus.add_animation("hover", "plus_hover")

    sfx_minus = AnimatedButton(SpriteSheetAtlas(assets["images/ui/menu/Minus.png"], assets["images/ui/menu/Minus.xml"]),
                               name="sfx_minus", pos=(310, 360))
    sfx_minus.add_animation("normal", "minus_normal")
    sfx_minus.add_animation("hover", "minus_hover")

    sfx_plus = AnimatedButton(SpriteSheetAtlas(assets["images/ui/menu/Plus.png"], assets["images/ui/menu/Plus.xml"]),
                              name="sfx_plus", pos=(470, 360))
    sfx_plus.add_animation("normal", "plus_normal")
    sfx_plus.add_animation("hover", "plus_hover")

    fullscreen_btn = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/menu/Checkbox.png"], assets["images/ui/menu/Checkbox.xml"]),
        name="fullscreen", pos=(470, 410))
    fullscreen_btn.add_animation("unchecked", "tick_normal")
    fullscreen_btn.add_animation("checked", "ticked")

    shader_btn = AnimatedButton(
        SpriteSheetAtlas(assets["images/ui/menu/Checkbox.png"], assets["images/ui/menu/Checkbox.xml"]),
        name="shader", pos=(470, 460))
    shader_btn.add_animation("unchecked", "tick_normal")
    shader_btn.add_animation("checked", "ticked")

    back_btn = AnimatedButton(SpriteSheetAtlas(assets["images/ui/menu/Back.png"], assets["images/ui/menu/Back.xml"]),
                              name="back", pos=(400, 525))
    back_btn.add_animation("normal", "normal_back")
    back_btn.add_animation("hover", "hover_back")

    buttons = [music_minus, music_plus, sfx_minus, sfx_plus, fullscreen_btn, shader_btn, back_btn]

    scene_surface = pygame.Surface((w, h))

    running = True
    while running:
        dt = clock.tick(main.fps)
        # Jumps when going back, so might aswell pause it to have a smoother lookin thing...
        #offset_x += scroll_x * (dt / 16.67)
        #offset_y += scroll_y * (dt / 16.67)

        mouse_pos = pygame.mouse.get_pos()

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

        screen.fill((0, 0, 0))
        cols = w // tile_size + 8
        rows = h // tile_size + 8

        for row in range(rows):
            for col in range(cols):
                x = col * tile_size + offset_x
                y = row * tile_size + offset_y
                scene_surface.blit(grid_img, (x, y))

        time_elapsed = pygame.time.get_ticks() / 750
        float_offset = math.sin(time_elapsed * 2 * math.pi / 3) * 10
        rect = logo_img.get_rect(center=(400, 125 + float_offset))
        scene_surface.blit(logo_img, rect)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
                for btn in buttons:
                    if btn.get_rect().collidepoint(e.pos):
                        if btn.name == "music_minus":
                            volumes["music"] = max(0, volumes["music"] - 0.1)
                            menu_music.set_volume(volumes["music"])
                        elif btn.name == "music_plus":
                            volumes["music"] = min(1, volumes["music"] + 0.1)
                            menu_music.set_volume(volumes["music"])
                        elif btn.name == "sfx_minus":
                            volumes["sfx"] = max(0, volumes["sfx"] - 0.1)
                            pygame.mixer.music.set_volume(volumes["sfx"])
                        elif btn.name == "sfx_plus":
                            volumes["sfx"] = min(1, volumes["sfx"] + 0.1)
                            pygame.mixer.music.set_volume(volumes["sfx"])
                        elif btn.name == "fullscreen":
                            fullscreen = not fullscreen
                            pygame.display.set_mode((w, h), pygame.FULLSCREEN if fullscreen else 0)
                        elif btn.name == "shader":
                            shader = not shader
                        elif btn.name == "back":
                            return volumes, fullscreen, shader

        music_text = font.render(f"Music Volume", True, (255,255,255))
        music_text_val = font.render(f"{int(volumes['music']*100)}%", True, (255,255,255))

        sfx_text = font.render(f"SFX Volume", True, (255,255,255))
        sfx_text_val = font.render(f"{int(volumes['sfx']*100)}%", True, (255,255,255))

        fullscreen_text = font.render(f"Fullscreen", True, (255,255,255))

        shader_text = font.render(f"Shader", True, (255,255,255))

        scene_surface.blit(music_text, (320, 243))
        scene_surface.blit(music_text_val, (380, 280))

        scene_surface.blit(sfx_text, (330, 324))
        scene_surface.blit(sfx_text_val, (380, 360))

        scene_surface.blit(fullscreen_text, (300, 420))
        scene_surface.blit(shader_text, (310, 470))

        for btn in buttons:
            # this is so hacky, so fucking hacky and bad, never do this again
            # im doing it cause i dont know how else to do it
            if btn.name == "fullscreen":
                btn.play("checked" if fullscreen else "unchecked")
                btn.update(dt, (-9999, -9999))
            elif btn.name == "shader":
                btn.play("checked" if shader else "unchecked")
                btn.update(dt, (-9999, -9999))
            else:
                btn.update(dt, mouse_pos)
            btn.draw(scene_surface)

        if shader:
            chroma.apply(screen, scene_surface)
        else:
            screen.blit(scene_surface, (0, 0))

        draw_fps(screen, clock)
        pygame.display.flip()

    return volumes, fullscreen, shader