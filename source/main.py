import pygame
import os
import xml.etree.ElementTree as ET
from source.menus import splash

pygame.init()

w, h = 800, 600
screen = pygame.display.set_mode((w, h))
icon = pygame.image.load("../assets/images/icon.png").convert_alpha()
pygame.display.set_icon(icon)

pygame.display.set_caption("Loading...")
clock = pygame.time.Clock()
font = pygame.font.Font("../assets/fonts/undertalesans.ttf", 30)

fps = 60
assets = {}

volumes = {
    "music": 0.5,
    "sfx": 0.5
}

# hacky fix to keep background grid consistant
scroll_state = {
    "offset_x": -64,
    "offset_y": -64,
    "scroll_x": -0.5,
    "scroll_y": -0.5,
}

difficulty = "easy"

fullscreen = False
shader = True
shaderVal = 3 # to actually set

fade_speed = 200 # for alpha fading

def load_all_assets(folder): # prefetching
    a = {}
    for root, _, files in os.walk(folder):
        for f in files:
            p = os.path.join(root, f)
            rp = os.path.relpath(p, folder).replace("\\", "/")
            print("loading:", rp)
            try:
                if f.lower().endswith(".png"):
                    a[rp] = pygame.image.load(p).convert_alpha()
                elif f.lower().endswith((".ogg", ".wav")):
                    a[rp] = pygame.mixer.Sound(p)
                elif f.lower().endswith(".xml"):
                    tree = ET.parse(p)
                    a[rp] = tree.getroot()
            except Exception as e:
                print(f"couldn't load {f}: {e}")
    return a

def draw_fps(screen, clock): # style check lol
    fps_text = font.render(f"{int(clock.get_fps())} FPS", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

def main():
    global assets
    assets = load_all_assets(os.path.join("..", "assets"))

    splash.run(screen, assets, clock, draw_fps)

if __name__ == "__main__":
    main()
