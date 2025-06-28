import pygame

class PieceType:
    PLAYER = "player"
    ENEMY = "enemy"
    BOMB = "bomb"

class Piece(pygame.sprite.Sprite):
    def __init__(self, type, pos, image):
        super().__init__()
        self.type = type
        self.owner = type
        self.image = image
        self.rect = self.image.get_rect(topleft=pos)
