import pygame
from pygame.sprite import Sprite


class Alien(Sprite):
    """Class showing one alies ship"""

    def __init__(self, ai_game):
        """Initialization alien and define his position"""
        super().__init__()
        self.screen = ai_game.screen

        # Load alien image and rect
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        # Define alien position near top left corner ( alien height and width from corner)
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        # Storage precision alien position
        self.x = float(self.rect.x)
