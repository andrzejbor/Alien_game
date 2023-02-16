import pygame


class Ship:
    """Class for managing ship"""

    def __init__(self, ai_game):
        """Initialization ship and default position"""

        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        # Load ship image and rect
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()

        # New ship appear on screen bottom
        self.rect.midbottom = self.screen_rect.midbottom

    def blitme(self):
        """Display ship in actual position"""
        self.screen.blit(self.image, self.rect)
