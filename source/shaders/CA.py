import pygame

# faked it because opengl is ass to work it
# besides its not worth doing opengl on this project
class Abber:
    def __init__(self, offset=3):
        self.offset = offset

    def tint_surface(self, surf, color):
        tinted = surf.copy()
        tinted.fill(color, special_flags=pygame.BLEND_MULT)
        return tinted

    def apply(self, screen, scene_surface):
        red_surf = self.tint_surface(scene_surface, (255, 0, 0))
        green_surf = self.tint_surface(scene_surface, (0, 255, 0))
        blue_surf = self.tint_surface(scene_surface, (0, 0, 255))

        screen.fill((0, 0, 0))

        screen.blit(red_surf, (-self.offset, 0), special_flags=pygame.BLEND_ADD)
        screen.blit(green_surf, (0, 0), special_flags=pygame.BLEND_ADD)
        screen.blit(blue_surf, (self.offset, 0), special_flags=pygame.BLEND_ADD)
